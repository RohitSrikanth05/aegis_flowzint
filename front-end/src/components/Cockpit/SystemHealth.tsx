import { motion } from "framer-motion";

const items = [
  { k: "Backend", v: "Online" },
  { k: "Trust Engine", v: "Online" },
  { k: "Learning Engine", v: "Online" },
  { k: "LLM", v: "Connected" },
  { k: "Database", v: "Healthy" },
];

export function SystemHealth() {
  return (
    <div className="grid grid-cols-2 gap-2">
      {items.map((i) => (
        <div
          key={i.k}
          className="flex items-center justify-between rounded-md border border-white/5 bg-white/[0.02] px-2.5 py-1.5"
        >
          <span className="truncate text-[10px] uppercase tracking-wider text-white/45">
            {i.k}
          </span>
          <span className="flex items-center gap-1.5">
            <motion.span
              className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.8)]"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 1.6, repeat: Infinity }}
            />
            <span className="text-[10px] font-semibold text-emerald-300">{i.v}</span>
          </span>
        </div>
      ))}
    </div>
  );
}