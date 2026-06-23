import { useCallback, useEffect, useState } from "react";
import type { ChatMessage } from "@/types/chat";

export interface ChatSession {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
  messages: ChatMessage[];
}

const KEY = "aegis.sessions.v1";

function read(): ChatSession[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as ChatSession[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function write(list: ChatSession[]) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(KEY, JSON.stringify(list));
}

export function useSessions() {
  const [sessions, setSessions] = useState<ChatSession[]>(() => read());

  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === KEY) setSessions(read());
    };
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