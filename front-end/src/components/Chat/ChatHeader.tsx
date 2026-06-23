import { Shield } from "lucide-react";
import { motion } from "framer-motion";
import { SessionsSheet } from "./SessionsSheet";

export function ChatHeader({ sessionId, sessionLabel }: { sessionId?: string; sessionLabel?: string }) {
  return (
    <div className="flex items-center justify-between border-b border-[var(--color-aegis-border)] px-6 py-4">
      <div className="flex min-w-0 items-center gap-3">
        <SessionsSheet activeId={sessionId} />
        <div className="relative grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-indigo-500/30 to-cyan-400/20 ring-1 ring-white/10">
          <Shield className="h-5 w-5 text-cyan-300" />
          <div className="absolute inset-0 rounded-xl bg-cyan-400/10 blur-xl" />
        </div>
        <div className="min-w-0">
          <div className="text-base font-bold tracking-wide text-white">AEGIS</div>
          <div className="truncate text-[10px] uppercase tracking-[0.18em] text-white/40">
            {sessionLabel ?? "Adaptive Enterprise Guardian Intelligence System"}
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5">
        <span className="relative flex h-2 w-2">
          <motion.span
            className="absolute inline-flex h-full w-full rounded-full bg-emerald-400"
            animate={{ opacity: [0.4, 1, 0.4], scale: [1, 1.6, 1] }}
            transition={{ duration: 1.8, repeat: Infinity }}
          />
          <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
        </span>
        <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-emerald-300">
          Secure Session
        </span>
      </div>
    </div>
  );
}