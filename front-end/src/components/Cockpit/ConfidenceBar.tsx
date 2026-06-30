import { motion } from "framer-motion";

export function ConfidenceBar({ value = 87 }: { value?: number }) {
  return (
    <div>
      <div className="mb-2 flex items-baseline justify-between">
        <div className="text-[10px] font-semibold uppercase tracking-[0.22em] text-white/50">
          AI Confidence
        </div>
        <div className="text-sm font-bold tabular-nums text-cyan-300">{value}%</div>
      </div>
      <div className="relative h-2 overflow-hidden rounded-full bg-white/[0.05]">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-blue-500 via-cyan-400 to-cyan-300 shadow-[0_0_16px_rgba(34,211,238,0.55)]"
        />
      </div>
      <p className="mt-2 text-[10px] leading-relaxed text-white/35">
        Confidence derived from knowledge coverage and reasoning certainty.
      </p>
    </div>
  );
}