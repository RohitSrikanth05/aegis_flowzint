import { useEffect, useMemo, useRef, useState, useCallback } from "react";
import { useNavigate } from "@tanstack/react-router";
import { ChatHeader } from "./ChatHeader";
import { ChatMessages } from "./ChatMessages";
import { ChatInput } from "./ChatInput";
import { Cockpit } from "@/components/Cockpit/Cockpit";
import type { ChatMessage } from "@/types/chat";
import { deriveTitle, loadSession, useSessions, type ChatSession } from "@/hooks/useSessions";
import { motion } from "framer-motion";
import { ShieldCheck, Sparkles, Zap, BarChart3, TrendingUp, Map, Users } from "lucide-react";
import type { SecurityEvent, LearningItem } from "@/types/trust";
import type { ActivityEvent } from "@/types/activity";
import type { SourceDoc, PriorityRow } from "@/types/product_intel";

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
  // Product Intelligence fields
  route: string | null;
  sources: SourceDoc[] | null;
  priority_table: PriorityRow[] | null;
}

async function callChatAPI(
  message: string,
  sessionId: string,
  username?: string | null,
): Promise<ChatAPIResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId, username }),
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
      PRODUCT_INTEL: "intel",
    };
    acts.push({
      id: crypto.randomUUID(),
      kind: kindMap[intent] ?? "info",
      time: now,
      label: `${intent === "PRODUCT_INTEL" ? "Product Intelligence" : intent} Intent Detected`,
    });
  }

  for (const ev of events) {
    const lower = ev.toLowerCase();
    let kind: ActivityEvent["kind"] = "info";
    if (lower.includes("threat") || lower.includes("detected")) kind = "alert";
    else if (lower.includes("drop") || lower.includes("mode:")) kind = "warn";
    else if (lower.includes("gap") || lower.includes("learning")) kind = "learn";
    else if (lower.includes("product intelligence") || lower.includes("route:") || lower.includes("product signal")) kind = "intel";
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

import { useAuth } from "@/hooks/useAuth";

// ── ChatView ─────────────────────────────────────────────────────────────────
export function ChatView({ sessionId, isAdmin = false }: { sessionId?: string; isAdmin?: boolean }) {
  const navigate = useNavigate();
  const { username } = useAuth();
  const { upsert } = useSessions();
  const [activeId, setActiveId] = useState<string | undefined>(sessionId);
  const [title, setTitle] = useState<string>("New session");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [typing, setTyping] = useState(false);
  const [isError, setIsError] = useState(false);
  const persistedRef = useRef(false);

  // Cockpit state — live from API
  const [trustScore, setTrustScore] = useState<number>(100);
  const [overallTrustScore, setOverallTrustScore] = useState<number>(100);
  const [userSessions, setUserSessions] = useState<UserSessionSummary[]>([]);
  const [confidenceScore, setConfidenceScore] = useState<number>(87);
  const [mode, setMode] = useState<string>("NORMAL");
  const [intent, setIntent] = useState<string>("SALES");
  const [activityFeed, setActivityFeed] = useState<ActivityEvent[]>([]);
  const [securityEvents, setSecurityEvents] = useState<SecurityEvent[]>([]);
  const [learningItem, setLearningItem] = useState<LearningItem | null>(null);

  // Fetch admin sessions summary when in admin mode
  const fetchAdminSessions = useCallback(async () => {
    if (!isAdmin) return;
    try {
      let res = await fetch(`${API_BASE}/admin/sessions`);
      if (!res.ok) {
        res = await fetch(`${API_BASE}/sessions`);
      }
      if (res.ok) {
        const data = await res.json();
        setOverallTrustScore(data.overall_trust_score ?? 100);
        setUserSessions(data.users ?? data.sessions ?? []);
        if (data.overall_confidence_score != null) {
          setConfidenceScore(data.overall_confidence_score);
        }
        if (Array.isArray(data.system_activities) && data.system_activities.length > 0) {
          setActivityFeed(data.system_activities);
        }
      }
    } catch (e) {
      console.warn("Failed to fetch admin sessions summary:", e);
    }
  }, [isAdmin]);

  useEffect(() => {
    if (!isAdmin) return;
    fetchAdminSessions();
    const timer = setInterval(fetchAdminSessions, 4000);
    return () => clearInterval(timer);
  }, [isAdmin, fetchAdminSessions]);

  // Load existing session if routed
  useEffect(() => {
    if (sessionId) {
      const s = loadSession(sessionId);
      if (s) {
        setActiveId(s.id);
        setTitle(s.title);
        setMessages(s.messages);
        persistedRef.current = true;
      } else if (activeId !== sessionId) {
        // Only redirect home if this session truly doesn't exist and we're not currently creating it
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
        const userPrefix = username ? `session-${username}` : null;
        sid = userPrefix ?? crypto.randomUUID();
        isNew = true;
        setActiveId(sid);
        setTitle(deriveTitle(text));
      }
      setMessages((m) => [...m, userMsg]);
      setTyping(true);

      try {
        const data = await callChatAPI(text, sid!, username);

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
          // Product Intelligence
          route: data.route ?? undefined,
          sources: data.sources ?? undefined,
          priorityTable: data.priority_table ?? undefined,
        };

        setMessages((m) => [...m, botMsg]);
        fetchAdminSessions();
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

      <main className={`relative grid h-screen ${
        isAdmin
          ? "grid-cols-1 lg:grid-cols-[1.85fr_1fr] xl:grid-cols-[2fr_1fr]"
          : "grid-cols-1"
      }`}>
        <section className="flex h-full min-h-0 flex-col">
          <ChatHeader sessionId={activeId} sessionLabel={activeId ? title : undefined} isAdmin={isAdmin} />
          {showLanding ? <Landing isAdmin={isAdmin} /> : <ChatMessages messages={messages} typing={typing} />}
          <ChatInput onSend={handleSend} disabled={typing} />
        </section>
        {isAdmin && (
          <Cockpit
            trustScore={trustScore}
            overallTrustScore={overallTrustScore}
            userSessions={userSessions}
            confidenceScore={confidenceScore}
            mode={mode}
            intent={intent}
            activityFeed={activityFeed}
            securityEvents={securityEvents}
            learningItem={learningItem}
          />
        )}
      </main>
    </div>
  );
}

function Landing({ isAdmin = false }: { isAdmin?: boolean }) {
  const suggestions = useMemo(
    () => [
      // ── Security / Customer Service ──────────────────────────────────────
      {
        icon: ShieldCheck,
        title: "Verify a customer request",
        sub: "Run a trust + intent scan before acting",
        color: "text-cyan-300",
      },
      {
        icon: Sparkles,
        title: "Explain a premium plan",
        sub: "Sales mode, manipulation-resistant",
        color: "text-purple-300",
      },
      {
        icon: Zap,
        title: "Handle a refund inquiry",
        sub: "Support mode with escalation triggers",
        color: "text-amber-300",
      },
      // ── Product Intelligence ─────────────────────────────────────────────
      {
        icon: Users,
        title: "What are the top customer pain points?",
        sub: "Evidence-backed pain point analysis",
        color: "text-rose-300",
      },
      {
        icon: BarChart3,
        title: "Which features should we prioritize?",
        sub: "Multi-factor scoring across all signals",
        color: "text-indigo-300",
      },
      {
        icon: TrendingUp,
        title: "What are competitors doing that we are not?",
        sub: "Competitor gap analysis with threat levels",
        color: "text-emerald-300",
      },
      {
        icon: Map,
        title: "Generate a Q3 roadmap.",
        sub: "Monthly themes, dependencies, and risks",
        color: "text-sky-300",
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
          {isAdmin ? "Admin · Secure Session" : "New Secure Session"}
        </div>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-white">
          How can AEGIS help today?
        </h1>
        <p className="mt-2 text-sm text-white/50">
          Every message is inspected by the trust engine. Ask a customer service or product intelligence question.
        </p>

        <div className="mt-8 grid gap-2 text-left">
          {suggestions.map((s, i) => (
            <motion.div
              key={s.title}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.05 }}
              className="group flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] px-4 py-3 transition hover:border-cyan-400/30 hover:bg-white/[0.04]"
            >
              <div className={`grid h-9 w-9 place-items-center rounded-lg bg-white/[0.04] ring-1 ring-white/10 ${s.color}`}>
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