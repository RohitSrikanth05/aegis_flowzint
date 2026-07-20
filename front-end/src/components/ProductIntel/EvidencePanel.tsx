import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp, Database } from "lucide-react";
import type { SourceDoc } from "@/types/product_intel";

// ── Source type colour palette ────────────────────────────────────────────────
const SOURCE_COLORS: Record<string, { dot: string; badge: string; label: string }> = {
  customer_feedback: {
    dot: "bg-purple-400",
    badge: "border-purple-500/30 bg-purple-500/10 text-purple-300",
    label: "Customer Feedback",
  },
  jira_tickets: {
    dot: "bg-blue-400",
    badge: "border-blue-500/30 bg-blue-500/10 text-blue-300",
    label: "Jira Ticket",
  },
  support_cases: {
    dot: "bg-orange-400",
    badge: "border-orange-500/30 bg-orange-500/10 text-orange-300",
    label: "Support Case",
  },
  competitor_insights: {
    dot: "bg-rose-400",
    badge: "border-rose-500/30 bg-rose-500/10 text-rose-300",
    label: "Competitor Insight",
  },
  usage_analytics: {
    dot: "bg-emerald-400",
    badge: "border-emerald-500/30 bg-emerald-500/10 text-emerald-300",
    label: "Usage Analytics",
  },
};

const DEFAULT_COLOR = {
  dot: "bg-sky-400",
  badge: "border-sky-500/30 bg-sky-500/10 text-sky-300",
  label: "Source",
};

function getColor(sourceType: string) {
  return SOURCE_COLORS[sourceType] ?? DEFAULT_COLOR;
}

// ── Single evidence card ──────────────────────────────────────────────────────
function SourceCard({ doc }: { doc: SourceDoc }) {
  const c = getColor(doc.source_type);
  return (
    <div className="rounded-xl border border-white/[0.06] bg-white/[0.025] px-3 py-2.5">
      <div className="flex items-center gap-2 flex-wrap">
        <span className={`flex items-center gap-1.5 rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider ${c.badge}`}>
          <span className={`h-1.5 w-1.5 rounded-full ${c.dot}`} />
          {c.label}
        </span>
        {doc.product_area && (
          <span className="rounded-full border border-white/10 bg-white/[0.04] px-2 py-0.5 text-[9px] text-white/50 uppercase tracking-wider">
            {doc.product_area}
          </span>
        )}
        {doc.severity_or_priority && (
          <span className="rounded-full border border-white/10 bg-white/[0.04] px-2 py-0.5 text-[9px] text-white/40 uppercase tracking-wider">
            {doc.severity_or_priority}
          </span>
        )}
      </div>
      {doc.page_content && (
        <p className="mt-2 text-[11px] leading-relaxed text-white/55 line-clamp-3">
          {doc.page_content}
        </p>
      )}
    </div>
  );
}

// ── EvidencePanel ─────────────────────────────────────────────────────────────
interface EvidencePanelProps {
  sources: SourceDoc[];
}

export function EvidencePanel({ sources }: EvidencePanelProps) {
  const [open, setOpen] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3">
      {/* Toggle button */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center gap-2 rounded-xl border border-white/[0.07] bg-white/[0.02] px-3 py-2 text-left transition hover:border-violet-400/30 hover:bg-white/[0.035]"
      >
        <Database className="h-3.5 w-3.5 shrink-0 text-violet-400" />
        <span className="flex-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/50">
          Retrieved Evidence
        </span>
        <span className="text-[10px] text-white/30">{sources.length} source{sources.length !== 1 ? "s" : ""}</span>
        {open ? (
          <ChevronUp className="h-3.5 w-3.5 text-white/30" />
        ) : (
          <ChevronDown className="h-3.5 w-3.5 text-white/30" />
        )}
      </button>

      {/* Evidence cards */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="mt-2 space-y-2 pl-1">
              {sources.map((doc, i) => (
                <SourceCard key={i} doc={doc} />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
