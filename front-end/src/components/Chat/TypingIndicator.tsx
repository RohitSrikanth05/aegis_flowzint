import { motion } from "framer-motion";

export function TypingIndicator() {
  return (
    <div className="flex items-center gap-2 px-1 py-2 text-xs text-white/60">
      <div className="flex gap-1">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            className="h-1.5 w-1.5 rounded-full bg-cyan-300"
            animate={{ opacity: [0.2, 1, 0.2], y: [0, -2, 0] }}
            transition={{ duration: 1, repeat: Infinity, delay: i * 0.15 }}
          />
        ))}
      </div>
      <span className="uppercase tracking-[0.2em]">AEGIS is thinking…</span>
    </div>
  );
}