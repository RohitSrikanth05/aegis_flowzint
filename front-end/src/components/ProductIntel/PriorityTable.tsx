import { BarChart3 } from "lucide-react";
import type { PriorityRow } from "@/types/product_intel";

// ── Recommendation badge colours ──────────────────────────────────────────────
function recBadge(recommendation: string): string {
  if (recommendation.toLowerCase().includes("immediately"))
    return "border-rose-500/40 bg-rose-500/10 text-rose-300";
  if (recommendation.toLowerCase().includes("next"))
    return "border-amber-500/40 bg-amber-500/10 text-amber-300";
  if (recommendation.toLowerCase().includes("monitor"))
    return "border-yellow-500/40 bg-yellow-500/10 text-yellow-300";
  return "border-white/10 bg-white/[0.04] text-white/40";
}

function scoreBar(value: number, max: number = 20) {
  const pct = Math.min(100, Math.round((value / max) * 100));
  return (
    <div className="flex items-center gap-2">
      <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/[0.06]">
        <div
          className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="w-6 text-right text-[10px] tabular-nums text-white/40">{value}</span>
    </div>
  );
}

// ── PriorityTable ─────────────────────────────────────────────────────────────
interface PriorityTableProps {
  rows: PriorityRow[];
}

export function PriorityTable({ rows }: PriorityTableProps) {
  if (!rows || rows.length === 0) return null;

  return (
    <div className="mt-3 rounded-2xl border border-white/[0.08] bg-white/[0.025] overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-white/[0.06] px-4 py-3">
        <BarChart3 className="h-3.5 w-3.5 text-indigo-400" />
        <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-white/50">
          Product Area Priority Scores
        </span>
      </div>

      {/* Rows */}
      <div className="divide-y divide-white/[0.04]">
        {rows.map((row, i) => (
          <div key={row.product_area} className="px-4 py-3">
            {/* Area + rank + recommendation */}
            <div className="flex items-center justify-between gap-3 mb-2">
              <div className="flex items-center gap-2">
                <span className="text-[10px] tabular-nums text-white/25 w-4">#{i + 1}</span>
                <span className="text-sm font-semibold text-white">{row.product_area}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-white/60 tabular-nums">
                  {row.final_score}
                </span>
                <span className={`rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider ${recBadge(row.recommendation)}`}>
                  {row.recommendation}
                </span>
              </div>
            </div>

            {/* Mini score bars */}
            <div className="grid grid-cols-2 gap-x-4 gap-y-1 pl-6">
              <div>
                <div className="mb-0.5 text-[9px] uppercase tracking-wider text-white/25">Severity</div>
                {scoreBar(row.severity_score)}
              </div>
              <div>
                <div className="mb-0.5 text-[9px] uppercase tracking-wider text-white/25">Impact</div>
                {scoreBar(row.customer_impact_score)}
              </div>
              <div>
                <div className="mb-0.5 text-[9px] uppercase tracking-wider text-white/25">Competitor</div>
                {scoreBar(row.competitor_pressure_score)}
              </div>
              <div>
                <div className="mb-0.5 text-[9px] uppercase tracking-wider text-white/25">Frequency</div>
                {scoreBar(row.frequency_score, 5)}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
