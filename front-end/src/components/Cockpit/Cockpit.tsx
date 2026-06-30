import { motion } from "framer-motion";
import { TrustGauge } from "./TrustGauge";
import { ModeIndicator } from "./ModeIndicator";
import { ConfidenceBar } from "./ConfidenceBar";
import { ActivityFeed } from "./ActivityFeed";
import { LearningPanel } from "./LearningPanel";
import { SecurityCenter } from "./SecurityCenter";
import { SystemHealth } from "./SystemHealth";
import { useTrustScore } from "@/hooks/useTrustScore";
import { useMode } from "@/hooks/useMode";
import { dummyActivity, dummySecurity, dummyLearning } from "@/data/dummyActivity";

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

export function Cockpit() {
  const score = useTrustScore(92);
  const mode = useMode("sales");

  return (
    <aside className="flex h-full flex-col gap-4 overflow-y-auto border-l border-[var(--color-aegis-border)] bg-gradient-to-b from-white/[0.02] to-transparent p-4 [scrollbar-width:thin] lg:p-5">
      <div className="flex items-center justify-between">
        <div className="text-[10px] font-semibold uppercase tracking-[0.28em] text-white/45">
          Aegis Cockpit
        </div>
        <div className="text-[10px] uppercase tracking-[0.18em] text-white/30">v1.0 · Live</div>
      </div>

      <Section>
        <div className="grid place-items-center py-2">
          <TrustGauge score={score} />
          <div className="mt-2 text-[10px] uppercase tracking-[0.22em] text-white/40">
            Conversation Risk Analysis
          </div>
        </div>
      </Section>

      <Section title="Operating Mode">
        <ModeIndicator mode={mode} />
      </Section>

      <Section>
        <ConfidenceBar value={87} />
      </Section>

      <Section title="Live Agent Activity">
        <ActivityFeed events={[...dummyActivity].reverse()} />
      </Section>

      <Section title="Self Learning Engine">
        <LearningPanel item={dummyLearning} />
      </Section>

      <Section title="Security Center">
        <SecurityCenter events={dummySecurity} />
      </Section>

      <Section title="System Health">
        <SystemHealth />
      </Section>
    </aside>
  );
}