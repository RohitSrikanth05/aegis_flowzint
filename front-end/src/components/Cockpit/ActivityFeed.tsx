import { AnimatePresence, motion } from "framer-motion";
import type { ActivityEvent, ActivityKind } from "@/types/activity";

const dot: Record<ActivityKind, string> = {
  ok: "bg-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.7)]",
  warn: "bg-amber-400 shadow-[0_0_10px_rgba(245,158,11,0.7)]",
  alert: "bg-rose-400 shadow-[0_0_10px_rgba(244,63,94,0.7)]",
  info: "bg-sky-400 shadow-[0_0_10px_rgba(56,189,248,0.7)]",
  learn: "bg-indigo-400 shadow-[0_0_10px_rgba(99,102,241,0.7)]",
};

export function ActivityFeed({ events }: { events: ActivityEvent[] }) {
  return (
    <div className="max-h-56 overflow-y-auto pr-1 [scrollbar-width:thin]">
      <ul className="space-y-2">
        <AnimatePresence initial={false}>
          {events.map((e) => (
            <motion.li
              key={e.id}
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-3 rounded-lg border border-white/5 bg-white/[0.02] px-3 py-2"
            >
              <span className={`h-2 w-2 shrink-0 rounded-full ${dot[e.kind]}`} />
              <span className="w-14 shrink-0 text-[10px] uppercase tracking-wider text-white/35">
                {e.time}
              </span>
              <span className="truncate text-xs text-white/80">{e.label}</span>
            </motion.li>
          ))}
        </AnimatePresence>
      </ul>
    </div>
  );
}