import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, CheckCircle, XCircle, Loader2, ShieldCheck, RefreshCw, AlertTriangle } from "lucide-react";

const API_BASE = "http://localhost:8000";

interface LearningQueueItem {
  id: number;
  question: string;
  retrieved_context: Array<{ title: string; content: string; type: string; category: string }>;
  confidence: number;
  status: "pending" | "approved" | "rejected";
  timestamp: string;
}

export const Route = createFileRoute("/learning-queue")({
  head: () => ({
    meta: [
      { title: "AEGIS — Knowledge Learning Queue" },
      { name: "description", content: "Review and approve AI-detected knowledge gaps to improve the knowledge base." },
    ],
  }),
  component: LearningQueuePage,
});

function statusColor(status: string) {
  if (status === "approved") return "text-emerald-400 border-emerald-400/30 bg-emerald-500/10";
  if (status === "rejected") return "text-rose-400 border-rose-400/30 bg-rose-500/10";
  return "text-amber-400 border-amber-400/30 bg-amber-500/10";
}

function confidenceColor(c: number) {
  if (c >= 7) return "text-emerald-400";
  if (c >= 4) return "text-amber-400";
  return "text-rose-400";
}

function LearningQueuePage() {
  const [items, setItems] = useState<LearningQueueItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actioning, setActioning] = useState<Record<number, boolean>>({});
  const [approvedAnswers, setApprovedAnswers] = useState<Record<number, string>>({});

  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/learning-queue`);
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const data = await res.json();
      setItems(data.items);
    } catch (e: any) {
      setError("Cannot connect to AEGIS backend. Make sure FastAPI is running on port 8000.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleApprove = async (id: number) => {
    setActioning((p) => ({ ...p, [id]: true }));
    try {
      const res = await fetch(`${API_BASE}/learning-queue/${id}/approve`, { method: "POST" });
      if (!res.ok) throw new Error(`Status ${res.status}`);
      const data = await res.json();
      setApprovedAnswers((p) => ({ ...p, [id]: data.generated_answer }));
      setItems((prev) => prev.map((item) => (item.id === id ? { ...item, status: "approved" } : item)));
    } catch (e: any) {
      alert(`Approve failed: ${e.message}`);
    } finally {
      setActioning((p) => ({ ...p, [id]: false }));
    }
  };

  const handleReject = async (id: number) => {
    setActioning((p) => ({ ...p, [id]: true }));
    try {
      const res = await fetch(`${API_BASE}/learning-queue/${id}/reject`, { method: "POST" });
      if (!res.ok) throw new Error(`Status ${res.status}`);
      setItems((prev) => prev.map((item) => (item.id === id ? { ...item, status: "rejected" } : item)));
    } catch (e: any) {
      alert(`Reject failed: ${e.message}`);
    } finally {
      setActioning((p) => ({ ...p, [id]: false }));
    }
  };

  const pending = items.filter((i) => i.status === "pending");
  const processed = items.filter((i) => i.status !== "pending");

  return (
    <div className="min-h-screen bg-[#09090b] font-sans text-white">
      {/* Background glows */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute -left-40 top-10 h-[420px] w-[420px] rounded-full bg-indigo-600/20 blur-[140px]" />
        <div className="absolute right-0 top-1/3 h-[420px] w-[420px] rounded-full bg-cyan-500/15 blur-[140px]" />
      </div>

      <div className="relative z-10 mx-auto max-w-5xl px-6 py-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 flex items-center justify-between"
        >
          <div className="flex items-center gap-4">
            <a
              href="/"
              className="flex items-center gap-2 text-white/40 text-sm hover:text-white transition-colors"
            >
              <ShieldCheck className="h-4 w-4 text-cyan-400" />
              AEGIS
            </a>
            <span className="text-white/20">/</span>
            <div className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-indigo-400" />
              <span className="font-semibold text-white">Knowledge Learning Queue</span>
            </div>
          </div>

          <button
            onClick={fetchItems}
            className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.03] px-4 py-2 text-sm text-white/70 transition hover:border-white/20 hover:text-white"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh
          </button>
        </motion.div>

        {/* Stats bar */}
        <div className="mb-8 grid grid-cols-3 gap-4">
          {[
            { label: "Pending Review", value: pending.length, color: "text-amber-400" },
            { label: "Approved & Learned", value: items.filter((i) => i.status === "approved").length, color: "text-emerald-400" },
            { label: "Rejected", value: items.filter((i) => i.status === "rejected").length, color: "text-rose-400" },
          ].map((stat) => (
            <div
              key={stat.label}
              className="rounded-2xl border border-white/[0.08] bg-white/[0.03] p-4 text-center"
            >
              <div className={`text-3xl font-bold tabular-nums ${stat.color}`}>{stat.value}</div>
              <div className="mt-1 text-[10px] font-semibold uppercase tracking-[0.22em] text-white/40">
                {stat.label}
              </div>
            </div>
          ))}
        </div>

        {/* Error state */}
        {error && (
          <div className="mb-6 flex items-center gap-3 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-rose-300">
            <AlertTriangle className="h-5 w-5 shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {/* Loading state */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-8 w-8 animate-spin text-indigo-400" />
          </div>
        )}

        {/* Pending items */}
        {!loading && !error && (
          <>
            {pending.length > 0 && (
              <div className="mb-8">
                <h2 className="mb-4 text-[10px] font-semibold uppercase tracking-[0.25em] text-white/50">
                  Pending Review ({pending.length})
                </h2>
                <div className="space-y-4">
                  <AnimatePresence>
                    {pending.map((item) => (
                      <motion.div
                        key={item.id}
                        initial={{ opacity: 0, y: 8 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.97 }}
                        className="rounded-2xl border border-amber-500/20 bg-amber-500/[0.04] p-5"
                      >
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1 min-w-0">
                            <div className="mb-1 text-[9px] font-semibold uppercase tracking-[0.2em] text-amber-300/70">
                              Knowledge Gap
                            </div>
                            <div className="text-base font-semibold text-white">{item.question}</div>
                            <div className="mt-1 text-[10px] text-white/40">
                              Logged: {item.timestamp} · Confidence:{" "}
                              <span className={`font-bold ${confidenceColor(item.confidence)}`}>
                                {item.confidence}/10
                              </span>
                            </div>
                          </div>
                          {!actioning[item.id] ? (
                            <div className="flex shrink-0 gap-2">
                              <button
                                onClick={() => handleApprove(item.id)}
                                className="flex items-center gap-1.5 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-300 transition hover:bg-emerald-500/20"
                              >
                                <CheckCircle className="h-3.5 w-3.5" />
                                Approve & Learn
                              </button>
                              <button
                                onClick={() => handleReject(item.id)}
                                className="flex items-center gap-1.5 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-1.5 text-xs font-semibold text-rose-300 transition hover:bg-rose-500/20"
                              >
                                <XCircle className="h-3.5 w-3.5" />
                                Reject
                              </button>
                            </div>
                          ) : (
                            <Loader2 className="h-5 w-5 animate-spin text-white/40" />
                          )}
                        </div>

                        {/* Retrieved context preview */}
                        {item.retrieved_context.length > 0 && (
                          <div className="mt-4 space-y-2">
                            <div className="text-[9px] font-semibold uppercase tracking-[0.2em] text-white/35">
                              Retrieved Context (was insufficient)
                            </div>
                            {item.retrieved_context.slice(0, 2).map((c, i) => (
                              <div
                                key={i}
                                className="rounded-lg border border-white/[0.05] bg-white/[0.02] px-3 py-2 text-xs text-white/60"
                              >
                                <span className="font-semibold text-white/80">{c.title}: </span>
                                {c.content}
                              </div>
                            ))}
                          </div>
                        )}
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
              </div>
            )}

            {pending.length === 0 && !loading && (
              <div className="mb-8 flex flex-col items-center justify-center rounded-2xl border border-white/[0.06] bg-white/[0.02] py-16 text-center">
                <Brain className="mb-3 h-8 w-8 text-indigo-400/50" />
                <div className="text-sm text-white/40">No pending items. AEGIS is up to date!</div>
              </div>
            )}

            {/* Processed items */}
            {processed.length > 0 && (
              <div>
                <h2 className="mb-4 text-[10px] font-semibold uppercase tracking-[0.25em] text-white/50">
                  Processed ({processed.length})
                </h2>
                <div className="space-y-3">
                  {processed.map((item) => (
                    <div
                      key={item.id}
                      className="rounded-xl border border-white/[0.06] bg-white/[0.02] px-4 py-3"
                    >
                      <div className="flex items-center justify-between gap-4">
                        <div className="min-w-0">
                          <div className="truncate text-sm text-white/80">{item.question}</div>
                          {approvedAnswers[item.id] && (
                            <div className="mt-2 rounded-lg border border-emerald-500/20 bg-emerald-500/[0.04] px-3 py-2 text-xs text-white/70">
                              <span className="font-semibold text-emerald-300">Generated Answer: </span>
                              {approvedAnswers[item.id]}
                            </div>
                          )}
                        </div>
                        <span
                          className={`shrink-0 rounded-full border px-2.5 py-0.5 text-[9px] font-semibold uppercase tracking-wider ${statusColor(item.status)}`}
                        >
                          {item.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
