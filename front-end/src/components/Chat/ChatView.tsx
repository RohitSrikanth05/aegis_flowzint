import { useEffect, useMemo, useRef, useState, useCallback } from "react";
import { useNavigate } from "@tanstack/react-router";
import { ChatHeader } from "./ChatHeader";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import { Cockpit } from "@/components/Cockpit/Cockpit";
import type { ChatMessage } from "@/types/chat";
import { deriveTitle, loadSession, useSessions, type ChatSession } from "@/hooks/useSessions";
import { motion } from "framer-motion";
import { ShieldCheck, Sparkles, Zap } from "lucide-react";
import type { SecurityEvent, LearningItem } from "@/types/trust";
import type { ActivityEvent } from "@/types/activity";

const API_BASE = "http://localhost:8000";

function nowTime() {
  return new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
}

// ── API call ─────────────────────────────────────────────────────────────────
interface ChatAPIResponse {
  reply: string;
  intent: string;
  session_id: string;
  trust_score: number | null;
  confidence_score: number | null;
  mode: string | null;
  events: string[];
}

async function callChatAPI(
  message: string,
  sessionId: string,
): Promise<ChatAPIResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Backend error ${res.status}: ${err}`);
  }
  return res.json();
}

// ── Map backend events → ActivityEvent ───────────────────────────────────────
function eventsToActivity(events: string[], intent: string): ActivityEvent[] {
  const now = nowTime();
  const acts: ActivityEvent[] = [];

  if (intent) {
    const kindMap: Record<string, ActivityEvent["kind"]> = {
      SALES: "ok",
      SUPPORT: "info",
      CARE: "warn",
    };
    acts.push({
      id: crypto.randomUUID(),
      kind: kindMap[intent] ?? "info",
      time: now,
      label: `${intent} Intent Detected`,
    });
  }

  for (const ev of events) {
    const lower = ev.toLowerCase();
    let kind: ActivityEvent["kind"] = "info";
    if (lower.includes("threat") || lower.includes("detected")) kind = "alert";
    else if (lower.includes("drop") || lower.includes("mode:")) kind = "warn";
    else if (lower.includes("gap") || lower.includes("learning")) kind = "learn";
    else if (lower.includes("rag") || lower.includes("confidence")) kind = "info";

    acts.push({ id: crypto.randomUUID(), kind, time: now, label: ev });
  }

  return acts;
}

// ── Map events → SecurityEvents ───────────────────────────────────────────────
const THREAT_TO_SECURITY: Record<string, { label: string; severity: SecurityEvent["severity"] }> = {
  prompt_injection: { label: "Prompt Injection Attempt", severity: "high" },
  jailbreak: { label: "Jailbreak Attack", severity: "high" },
  refund_abuse: { label: "Refund Fraud Attempt", severity: "critical" },
  discount_probing: { label: "Discount Probing", severity: "medium" },
  data_extraction: { label: "Data Extraction Attempt", severity: "high" },
  tool_abuse: { label: "Tool Abuse Attempt", severity: "high" },
  credential_theft: { label: "Credential Theft Attempt", severity: "critical" },
  policy_evasion: { label: "Policy Override Request", severity: "medium" },
  fraud_abuse: { label: "Fraud / Manipulation Attempt", severity: "critical" },
};

function extractSecurityEvents(events: string[]): SecurityEvent[] {
  const evs: SecurityEvent[] = [];
  for (const ev of events) {
    const lower = ev.toLowerCase();
    for (const [key, cfg] of Object.entries(THREAT_TO_SECURITY)) {
      if (lower.includes(key.replace("_", " ")) || lower.includes(key)) {
        evs.push({
          id: crypto.randomUUID(),
          label: cfg.label,
          severity: cfg.severity,
          status: "Blocked",
        });
      }
    }
  }
  return evs;
}

// ── ChatView ─────────────────────────────────────────────────────────────────
export function ChatView({ sessionId }: { sessionId?: string }) {
  const navigate = useNavigate();
  const { upsert } = useSessions();
  const [activeId, setActiveId] = useState<string | undefined>(sessionId);
  const [title, setTitle] = useState<string>("New session");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [typing, setTyping] = useState(false);
  const [isError, setIsError] = useState(false);
  const persistedRef = useRef(false);

  // Cockpit state — live from API
  const [trustScore, setTrustScore] = useState<number>(100);
  const [confidenceScore, setConfidenceScore] = useState<number>(87);
  const [mode, setMode] = useState<string>("NORMAL");
  const [intent, setIntent] = useState<string>("SALES");
  const [activityFeed, setActivityFeed] = useState<ActivityEvent[]>([]);
  const [securityEvents, setSecurityEvents] = useState<SecurityEvent[]>([]);
  const [learningItem, setLearningItem] = useState<LearningItem | null>(null);

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

  const handleSend = useCallback(
    async (text: string) => {
      setIsError(false);

      // Optimistically add user message
      const userMsg: ChatMessage = {
        id: crypto.randomUUID(),
        role: "user",
        content: text,
        timestamp: nowTime(),
      };

      let sid = activeId;
      let isNew = false;
      if (!sid) {
        sid = crypto.randomUUID();
        isNew = true;
        setActiveId(sid);
        setTitle(deriveTitle(text));
      }
      setMessages((m) => [...m, userMsg]);
      setTyping(true);

      if (isNew) {
        setTimeout(() => navigate({ to: "/session/$id", params: { id: sid! } }), 50);
      }

      try {
        const data = await callChatAPI(text, sid!);

        // Update cockpit state
        if (data.trust_score !== null) setTrustScore(data.trust_score);
        if (data.confidence_score !== null) setConfidenceScore(data.confidence_score * 10); // scale 1-10 → 10-100%
        if (data.mode) setMode(data.mode);
        if (data.intent) setIntent(data.intent);

        // Activity feed
        const newActivity = eventsToActivity(data.events, data.intent);
        setActivityFeed((prev) => [...newActivity, ...prev].slice(0, 20));

        // Security events
        const newSecurity = extractSecurityEvents(data.events);
        if (newSecurity.length > 0) {
          setSecurityEvents((prev) => [...newSecurity, ...prev].slice(0, 10));
        }

        // Learning item
        const gapEvent = data.events.find((e) => e.toLowerCase().includes("knowledge gap"));
        if (gapEvent) {
          setLearningItem({
            id: crypto.randomUUID(),
            question: text,
            status: "Pending Review",
          });
        }

        // Determine tone for bot reply
        const hasThreat = data.events.some((e) => e.toLowerCase().includes("threat"));

        const botMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: "bot",
          content: data.reply,
          timestamp: nowTime(),
          tone: hasThreat ? "alert" : undefined,
          intent: data.intent,
          trustScore: data.trust_score ?? undefined,
          confidenceScore: data.confidence_score ?? undefined,
          mode: data.mode ?? undefined,
        };

        setMessages((m) => [...m, botMsg]);
      } catch (err) {
        const errMsg: ChatMessage = {
          id: crypto.randomUUID(),
          role: "bot",
          content:
            "⚠️ Unable to reach the AEGIS backend. Make sure the FastAPI server is running on http://localhost:8000.",
          timestamp: nowTime(),
          tone: "alert",
        };
        setMessages((m) => [...m, errMsg]);
        setIsError(true);
      } finally {
        setTyping(false);
      }
    },
    [activeId, navigate],
  );

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
          <ChatInput onSend={handleSend} disabled={typing} />
        </section>
        <Cockpit
          trustScore={trustScore}
          confidenceScore={confidenceScore}
          mode={mode}
          intent={intent}
          activityFeed={activityFeed}
          securityEvents={securityEvents}
          learningItem={learningItem}
        />
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