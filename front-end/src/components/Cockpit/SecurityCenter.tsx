import { motion } from "framer-motion";
import { ShieldAlert, Ban, AlertOctagon, Bug } from "lucide-react";
import type { SecurityEvent } from "@/types/trust";

const sevStyle: Record<SecurityEvent["severity"], string> = {
  low: "text-sky-300 border-sky-400/30 bg-sky-500/10",
  medium: "text-amber-300 border-amber-400/30 bg-amber-500/10",
  high: "text-orange-300 border-orange-400/30 bg-orange-500/10",
  critical: "text-rose-300 border-rose-400/40 bg-rose-500/15",
};

const icon: Record<string, typeof ShieldAlert> = {
  Blocked: Ban,
  Denied: ShieldAlert,
  Escalated: AlertOctagon,
  Resolved: Bug,
};

export function SecurityCenter({ events }: { events: SecurityEvent[] }) {
  return (
    <ul className="space-y-2">
      {events.map((e, idx) => {
        const Icon = icon[e.status] ?? ShieldAlert;
        const isCritical = e.severity === "critical";
        return (
          <motion.li
            key={e.id}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.06 }}
            className="group flex items-center justify-between gap-2 rounded-lg border border-white/5 bg-white/[0.02] px-3 py-2 transition hover:border-white/15 hover:bg-white/[0.04]"
          >
            <div className="flex min-w-0 items-center gap-2">
              <motion.div
                animate={isCritical ? { opacity: [1, 0.4, 1] } : {}}
                transition={{ duration: 1.4, repeat: Infinity }}
                className={`grid h-7 w-7 shrink-0 place-items-center rounded-md border ${sevStyle[e.severity]}`}
              >
                <Icon className="h-3.5 w-3.5" />
              </motion.div>
              <span className="truncate text-xs text-white/85">{e.label}</span>
            </div>
            <span
              className={`shrink-0 rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider ${sevStyle[e.severity]}`}
            >
              {e.status}
            </span>
          </motion.li>
        );
      })}
    </ul>
  );
}