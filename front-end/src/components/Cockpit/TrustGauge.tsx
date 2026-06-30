import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { useEffect, useState } from "react";
import { trustLabel } from "@/hooks/useTrustScore";

const SIZE = 220;
const STROKE = 14;
const R = (SIZE - STROKE) / 2;
const C = 2 * Math.PI * R;

export function TrustGauge({ score }: { score: number }) {
  const mv = useMotionValue(score);
  const [display, setDisplay] = useState(score);
  const dash = useTransform(mv, (v) => C - (C * v) / 100);
  const { label, color } = trustLabel(display);

  useEffect(() => {
    const ctrl = animate(mv, score, { duration: 1.1, ease: "easeOut" });
    const unsub = mv.on("change", (v) => setDisplay(Math.round(v)));
    return () => {
      ctrl.stop();
      unsub();
    };
  }, [score, mv]);

  return (
    <div className="relative grid place-items-center">
      <svg width={SIZE} height={SIZE} className="-rotate-90">
        <defs>
          <linearGradient id="trustGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.9" />
            <stop offset="100%" stopColor={color} stopOpacity="0.4" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="b" />
            <feMerge>
              <feMergeNode in="b" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        <circle cx={SIZE / 2} cy={SIZE / 2} r={R} stroke="rgba(255,255,255,0.06)" strokeWidth={STROKE} fill="none" />
        <motion.circle
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={R}
          stroke="url(#trustGrad)"
          strokeWidth={STROKE}
          strokeLinecap="round"
          fill="none"
          strokeDasharray={C}
          style={{ strokeDashoffset: dash, filter: "url(#glow)" }}
        />
      </svg>
      <div className="absolute inset-0 grid place-items-center text-center">
        <div>
          <div className="text-[10px] uppercase tracking-[0.25em] text-white/40">Trust Score</div>
          <div
            className="mt-1 text-6xl font-bold tabular-nums"
            style={{ color, textShadow: `0 0 30px ${color}55` }}
          >
            {display}
          </div>
          <div
            className="mt-1 text-[10px] font-semibold uppercase tracking-[0.22em]"
            style={{ color }}
          >
            {label}
          </div>
        </div>
      </div>
    </div>
  );
}