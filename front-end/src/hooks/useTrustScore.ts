import { useEffect, useState } from "react";

export function useTrustScore(initial = 92) {
  const [score, setScore] = useState(initial);
  useEffect(() => {
    const id = setInterval(() => {
      setScore((s) => {
        const delta = (Math.random() - 0.45) * 6;
        return Math.max(28, Math.min(99, Math.round(s + delta)));
      });
    }, 3200);
    return () => clearInterval(id);
  }, []);
  return score;
}

export function trustLabel(score: number) {
  if (score >= 80) return { label: "TRUSTED USER", color: "var(--color-trust-high)" };
  if (score >= 50) return { label: "ELEVATED RISK", color: "var(--color-trust-mid)" };
  return { label: "HOSTILE ACTOR", color: "var(--color-trust-low)" };
}