import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { ChatHeader } from "./ChatHeader";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import { Cockpit } from "@/components/Cockpit/Cockpit";
import type { ChatMessage } from "@/types/chat";
import { deriveTitle, loadSession, useSessions, type ChatSession } from "@/hooks/useSessions";
import { motion } from "framer-motion";
import { ShieldCheck, Sparkles, Zap } from "lucide-react";

function nowTime() {
  return new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

function botReply(text: string): ChatMessage {
  const lower = text.toLowerCase();
  const suspicious = /ignore|jailbreak|prompt|override|bypass|admin|sudo/.test(lower);
  if (suspicious) {
    return {
      id: crypto.randomUUID(),
      role: "bot",
      tone: "alert",
      content:
        "Suspicious behavior detected. Trust score reduced. This request has been escalated for human review.",
      timestamp: nowTime(),
    };
  }
  return {
    id: crypto.randomUUID(),
    role: "bot",
    content:
      "Got it. AEGIS is analyzing intent, scanning for manipulation patterns, and routing this through the right operating mode.",
    timestamp: nowTime(),
  };
}

export function ChatView({ sessionId }: { sessionId?: string }) {
  const navigate = useNavigate();
  const { upsert } = useSessions();
  const [activeId, setActiveId] = useState<string | undefined>(sessionId);
  const [title, setTitle] = useState<string>("New session");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [typing, setTyping] = useState(false);
  const persistedRef = useRef(false);

  // Load existing session if routed
  useEffect(() => {
    if (sessionId) {
      const s = loadSession(sessionId);
      if (s) {
        setActiveId(s.id);
        setTitle(s.title);
        setMessages(s.messages);
        persistedRef.current = true;
      } else {
        navigate({ to: "/" });
      }
    } else {
      setActiveId(undefined);
      setTitle("New session");
      setMessages([]);
      persistedRef.current = false;
    }
  }, [sessionId, navigate]);

  // Persist on change (after first message)
  useEffect(() => {
    if (!activeId || messages.length === 0) return;
    const session: ChatSession = {
      id: activeId,
      title,
      createdAt: persistedRef.current ? (loadSession(activeId)?.createdAt ?? Date.now()) : Date.now(),
      updatedAt: Date.now(),
      messages,
    };
    upsert(session);
    persistedRef.current = true;
  }, [activeId, title, messages, upsert]);

  const handleSend = (text: string) => {
    const user: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
      timestamp: nowTime(),
    };
    let id = activeId;
    let isNew = false;
    if (!id) {
      id = crypto.randomUUID();
      isNew = true;
      setActiveId(id);
      setTitle(deriveTitle(text));
    }
    setMessages((m) => [...m, user]);
    setTyping(true);
    setTimeout(() => {
      setMessages((m) => [...m, botReply(text)]);
      setTyping(false);
    }, 1400);
    if (isNew) {
      // Navigate after state update so route component picks up the session
      setTimeout(() => navigate({ to: "/session/$id", params: { id: id! } }), 50);
    }
  };

  const showLanding = !activeId && messages.length === 0;

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#09090b] font-sans text-white">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -left-40 top-10 h-[420px] w-[420px] rounded-full bg-indigo-600/20 blur-[140px]" />
        <div className="absolute right-0 top-1/3 h-[420px] w-[420px] rounded-full bg-cyan-500/15 blur-[140px]" />
        <div className="absolute bottom-0 left-1/3 h-[360px] w-[360px] rounded-full bg-violet-600/10 blur-[140px]" />
        <div
          className="absolute inset-0 opacity-[0.05]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.6) 1px,transparent 1px)",
            backgroundSize: "44px 44px",
            maskImage: "radial-gradient(ellipse at center, black 40%, transparent 75%)",
          }}
        />
      </div>

      <main className="relative grid h-screen grid-cols-1 lg:grid-cols-[1.85fr_1fr] xl:grid-cols-[2fr_1fr]">
        <section className="flex h-full min-h-0 flex-col">
          <ChatHeader sessionId={activeId} sessionLabel={activeId ? title : undefined} />
          {showLanding ? <Landing /> : <ChatMessages messages={messages} typing={typing} />}
          <ChatInput onSend={handleSend} />
        </section>
        <Cockpit />
      </main>
    </div>
  );
}

function Landing() {
  const suggestions = useMemo(
    () => [
      {
        icon: ShieldCheck,
        title: "Verify a customer request",
        sub: "Run a trust + intent scan before acting",
      },
      {
        icon: Sparkles,
        title: "Explain a premium plan",
        sub: "Sales mode, manipulation-resistant",
      },
      {
        icon: Zap,
        title: "Handle a refund inquiry",
        sub: "Support mode with escalation triggers",
      },
    ],
    [],
  );

  return (
    <div className="flex flex-1 items-center justify-center overflow-y-auto px-6 py-10">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-xl text-center"
      >
        <div className="mx-auto mb-6 grid h-16 w-16 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500/30 to-cyan-400/20 ring-1 ring-white/10">
          <ShieldCheck className="h-7 w-7 text-cyan-300" />
          <div className="absolute h-16 w-16 rounded-2xl bg-cyan-400/10 blur-2xl" />
        </div>
        <div className="text-[10px] font-semibold uppercase tracking-[0.3em] text-cyan-300/80">
          New Secure Session
        </div>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-white">
          How can AEGIS help today?
        </h1>
        <p className="mt-2 text-sm text-white/50">
          Every message is inspected by the trust engine. Start a conversation or open a previous
          session.
        </p>

        <div className="mt-8 grid gap-2 text-left">
          {suggestions.map((s, i) => (
            <motion.div
              key={s.title}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.06 }}
              className="group flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] px-4 py-3 transition hover:border-cyan-400/30 hover:bg-white/[0.04]"
            >
              <div className="grid h-9 w-9 place-items-center rounded-lg bg-white/[0.04] text-cyan-300 ring-1 ring-white/10">
                <s.icon className="h-4 w-4" />
              </div>
              <div className="min-w-0">
                <div className="text-sm font-medium text-white/90">{s.title}</div>
                <div className="text-xs text-white/40">{s.sub}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}