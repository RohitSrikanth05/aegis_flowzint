import { motion } from "framer-motion";
import { TrustGauge } from "./TrustGauge";
import { ModeIndicator } from "./ModeIndicator";
import { ConfidenceBar } from "./ConfidenceBar";
import { ActivityFeed } from "./ActivityFeed";
import { LearningPanel } from "./LearningPanel";
import { SecurityCenter } from "./SecurityCenter";
import { SystemHealth } from "./SystemHealth";
import { trustLabel } from "@/hooks/useTrustScore";
import type { SecurityEvent, LearningItem } from "@/types/trust";
import type { ActivityEvent } from "@/types/activity";
import type { Mode } from "@/types/trust";

// Map backend intent → Mode for display
function intentToMode(intent: string): Mode {
  const map: Record<string, Mode> = {
    SALES: "sales",
    SUPPORT: "support",
    CARE: "care",
  };
  return map[intent?.toUpperCase()] ?? "support";
}

// Map backend TrustMode → display badge color class
function trustModeClass(mode: string): string {
  if (mode === "LOCKDOWN") return "text-rose-400 border-rose-500/40 bg-rose-500/10";
  if (mode === "CAUTIOUS") return "text-amber-400 border-amber-500/40 bg-amber-500/10";
  return "text-emerald-400 border-emerald-500/40 bg-emerald-500/10";
}

interface CockpitProps {
  trustScore?: number;
  confidenceScore?: number;
  mode?: string;         // NORMAL | CAUTIOUS | LOCKDOWN
  intent?: string;       // SALES | SUPPORT | CARE
  activityFeed?: ActivityEvent[];
  securityEvents?: SecurityEvent[];
  learningItem?: LearningItem | null;
}

function Section({
  title,
  children,
}: {
  title?: string;
  children: React.ReactNode;
}) {
  return (
    <motion.section
      whileHover={{ y: -2 }}
      transition={{ type: "spring", stiffness: 220, damping: 20 }}
      className="rounded-2xl border border-white/[0.08] bg-white/[0.035] p-4 shadow-[0_8px_40px_rgba(0,0,0,0.35)] backdrop-blur-xl hover:border-white/[0.16]"
    >
      {title && (
        <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.22em] text-white/50">
          {title}
        </div>
      )}
      {children}
    </motion.section>
  );
}

export function Cockpit({
  trustScore = 100,
  confidenceScore = 87,
  mode = "NORMAL",
  intent = "SALES",
  activityFeed = [],
  securityEvents = [],
  learningItem = null,
}: CockpitProps) {
  const displayMode = intentToMode(intent);
  const { label: trustLbl, color: trustColor } = trustLabel(trustScore);

  return (
    <aside className="flex h-full flex-col gap-4 overflow-y-auto border-l border-[var(--color-aegis-border)] bg-gradient-to-b from-white/[0.02] to-transparent p-4 [scrollbar-width:thin] lg:p-5">
      <div className="flex items-center justify-between">
        <div className="text-[10px] font-semibold uppercase tracking-[0.28em] text-white/45">
          Aegis Cockpit
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider ${trustModeClass(mode)}`}
          >
            {mode}
          </span>
          <div className="text-[10px] uppercase tracking-[0.18em] text-white/30">v1.0 · Live</div>
        </div>
      </div>

      <Section>
        <div className="grid place-items-center py-2">
          <TrustGauge score={trustScore} />
          <div className="mt-2 text-[10px] uppercase tracking-[0.22em] text-white/40">
            Conversation Risk Analysis
          </div>
        </div>
      </Section>

      <Section title="Operating Mode">
        <ModeIndicator mode={displayMode} />
      </Section>

      <Section>
        <ConfidenceBar value={Math.round(confidenceScore)} />
      </Section>

      <Section title="Live Agent Activity">
        {activityFeed.length > 0 ? (
          <ActivityFeed events={activityFeed} />
        ) : (
          <div className="py-4 text-center text-xs text-white/30">No activity yet. Send a message.</div>
        )}
      </Section>

      {learningItem && (
        <Section title="Self Learning Engine">
          <LearningPanel item={learningItem} />
        </Section>
      )}

      {securityEvents.length > 0 && (
        <Section title="Security Center">
          <SecurityCenter events={securityEvents} />
        </Section>
      )}

      <Section title="System Health">
        <SystemHealth />
      </Section>
    </aside>
  );
}