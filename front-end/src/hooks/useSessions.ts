import { useCallback, useEffect, useState } from "react";
import type { ChatMessage } from "@/types/chat";

export interface ChatSession {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
  messages: ChatMessage[];
}

function getSessionKey(): string {
  if (typeof window === "undefined") return "aegis.sessions.guest.v1";
  const user = window.localStorage.getItem("aegis_username");
  return user ? `aegis.sessions.${user.trim().toLowerCase()}.v1` : "aegis.sessions.guest.v1";
}

function read(): ChatSession[] {
  if (typeof window === "undefined") return [];
  try {
    const key = getSessionKey();
    const raw = window.localStorage.getItem(key);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as ChatSession[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function write(list: ChatSession[]) {
  if (typeof window === "undefined") return;
  const key = getSessionKey();
  window.localStorage.setItem(key, JSON.stringify(list));
}

export function useSessions() {
  const [sessions, setSessions] = useState<ChatSession[]>(() => read());

  // Re-sync sessions when storage changes or user logs in / switches accounts
  useEffect(() => {
    setSessions(read());
    const onStorage = () => setSessions(read());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const upsert = useCallback((session: ChatSession) => {
    setSessions((prev) => {
      const next = [session, ...prev.filter((s) => s.id !== session.id)];
      next.sort((a, b) => b.updatedAt - a.updatedAt);
      write(next);
      return next;
    });
  }, []);

  const remove = useCallback((id: string) => {
    setSessions((prev) => {
      const next = prev.filter((s) => s.id !== id);
      write(next);
      return next;
    });
  }, []);

  const clear = useCallback(() => {
    write([]);
    setSessions([]);
  }, []);

  return { sessions, upsert, remove, clear };
}

export function loadSession(id: string): ChatSession | null {
  return read().find((s) => s.id === id) ?? null;
}

export function deriveTitle(text: string): string {
  const t = text.trim().replace(/\s+/g, " ");
  if (t.length <= 48) return t || "New session";
  return t.slice(0, 45) + "…";
}