import { AnimatePresence, motion } from "framer-motion";
import { ShoppingBag, Wrench, Heart } from "lucide-react";
import type { Mode } from "@/types/trust";

const cfg: Record<Mode, { label: string; color: string; Icon: typeof ShoppingBag }> = {
  sales: { label: "Sales Mode", color: "var(--color-sales)", Icon: ShoppingBag },
  support: { label: "Support Mode", color: "var(--color-support)", Icon: Wrench },
  care: { label: "Customer Care", color: "var(--color-care)", Icon: Heart },
};

export function ModeIndicator({ mode }: { mode: Mode }) {
  const { label, color, Icon } = cfg[mode];
  return (
    <div className="relative overflow-hidden rounded-xl border border-white/10 bg-white/[0.03] p-3">
      <AnimatePresence mode="wait">
        <motion.div
          key={mode}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.4 }}
          className="flex items-center gap-3"
        >
          <div
            className="grid h-10 w-10 shrink-0 place-items-center rounded-lg"
            style={{ background: `${color}22`, boxShadow: `0 0 24px ${color}55`, color }}
          >
            <Icon className="h-5 w-5" />
          </div>
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-[0.2em] text-white/40">Active Mode</div>
            <div className="truncate text-sm font-semibold" style={{ color }}>
              {label}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
      <motion.div
        key={mode + "-pulse"}
        initial={{ opacity: 0.4 }}
        animate={{ opacity: 0 }}
        transition={{ duration: 1.2 }}
        className="pointer-events-none absolute inset-0"
        style={{ background: `radial-gradient(circle at 30% 50%, ${color}33, transparent 60%)` }}
      />
    </div>
  );
}