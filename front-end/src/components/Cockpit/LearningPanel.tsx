import { motion } from "framer-motion";
import { Brain, ChevronRight } from "lucide-react";
import type { LearningItem } from "@/types/trust";

const flow = ["Unknown", "Pending Review", "Approved", "Learned"] as const;

export function LearningPanel({ item }: { item: LearningItem }) {
  const activeIdx = flow.indexOf(item.status);
  return (
    <div>
      <div className="rounded-xl border border-indigo-400/20 bg-indigo-500/[0.04] p-3">
        <div className="flex items-start gap-2">
          <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-indigo-500/20 text-indigo-300">
            <Brain className="h-4 w-4" />
          </div>
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-[0.2em] text-indigo-300/70">
              Knowledge Gap
            </div>
            <div className="truncate text-sm font-medium text-white">{item.question}</div>
            <div className="mt-0.5 text-[10px] uppercase tracking-wider text-white/40">
              AI Status: <span className="text-rose-300">Unknown</span> · Queued for Learning
            </div>
          </div>
        </div>
      </div>

      <div className="mt-3 flex items-center justify-between gap-1">
        {flow.map((s, i) => {
          const active = i <= activeIdx;
          return (
            <div key={s} className="flex flex-1 items-center gap-1">
              <motion.div
                animate={
                  active
                    ? { boxShadow: ["0 0 0 rgba(99,102,241,0)", "0 0 14px rgba(99,102,241,0.6)", "0 0 0 rgba(99,102,241,0)"] }
                    : {}
                }
                transition={{ duration: 2, repeat: Infinity }}
                className={[
                  "flex-1 rounded-md px-1.5 py-1 text-center text-[9px] font-semibold uppercase tracking-wider",
                  active
                    ? "border border-indigo-400/40 bg-indigo-500/15 text-indigo-200"
                    : "border border-white/5 bg-white/[0.02] text-white/30",
                ].join(" ")}
              >
                {s}
              </motion.div>
              {i < flow.length - 1 && <ChevronRight className="h-3 w-3 shrink-0 text-white/20" />}
            </div>
          );
        })}
      </div>

      <button className="mt-3 w-full rounded-lg border border-white/10 bg-white/[0.03] py-2 text-xs font-medium text-white/80 transition hover:border-indigo-400/40 hover:bg-indigo-500/10 hover:text-white">
        View Knowledge Queue →
      </button>
    </div>
  );
}