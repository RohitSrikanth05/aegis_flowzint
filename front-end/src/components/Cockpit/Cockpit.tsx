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

import { useState } from "react";
import { Users, User, ShieldAlert } from "lucide-react";

export interface UserSessionSummary {
  user_id?: string;
  username?: string;
  session_id: string;
  trust_score: number;
  mode: string;
  updated_at: string;
}

interface CockpitProps {
  trustScore?: number;
  overallTrustScore?: number;
  userSessions?: UserSessionSummary[];
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
  overallTrustScore = 100,
  userSessions = [],
  confidenceScore = 87,
  mode = "NORMAL",
  intent = "SALES",
  activityFeed = [],
  securityEvents = [],
  learningItem = null,
}: CockpitProps) {
  const [selectedUserId, setSelectedUserId] = useState<string>("overall");

  const displayMode = intentToMode(intent);

  // If specific user is selected from dropdown, find user's trust metrics
  const selectedUser = userSessions.find((u) => (u.user_id || u.session_id) === selectedUserId);
  const activeGaugeScore =
    selectedUserId === "overall"
      ? overallTrustScore
      : selectedUser
        ? selectedUser.trust_score
        : trustScore;

  const activeMode =
    selectedUserId === "overall"
      ? mode
      : selectedUser
        ? selectedUser.mode
        : mode;

  return (
    <aside className="flex h-full flex-col gap-4 overflow-y-auto border-l border-[var(--color-aegis-border)] bg-gradient-to-b from-white/[0.02] to-transparent p-4 [scrollbar-width:thin] lg:p-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="text-[10px] font-semibold uppercase tracking-[0.28em] text-white/45">
          Admin Cockpit
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`rounded-full border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-wider ${trustModeClass(activeMode)}`}
          >
            {activeMode}
          </span>
          <div className="text-[10px] uppercase tracking-[0.18em] text-white/30">v1.0 · Live</div>
        </div>
      </div>

      {/* User Trust Inspector Dropdown (Userwise) */}
      <Section title="User Trust Inspector">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            {selectedUserId === "overall" ? (
              <Users className="h-4 w-4 text-cyan-400" />
            ) : (
              <User className="h-4 w-4 text-amber-400" />
            )}
            <select
              value={selectedUserId}
              onChange={(e) => setSelectedUserId(e.target.value)}
              className="flex-1 rounded-xl border border-white/10 bg-white/[0.06] py-1.5 px-2.5 text-xs text-white outline-none transition focus:border-cyan-400/50"
            >
              <option value="overall" className="bg-[#111113] text-white">
                🌐 All Users (System Average: {overallTrustScore}%)
              </option>
              {userSessions.map((u) => {
                const uid = u.user_id || u.session_id;
                const uname = u.username || u.session_id;
                return (
                  <option key={uid} value={uid} className="bg-[#111113] text-white">
                    👤 {uname} ({u.trust_score}% · {u.mode})
                  </option>
                );
              })}
            </select>
          </div>

          <div className="text-[9px] text-white/40 flex items-center justify-between pt-1">
            <span>
              {selectedUserId === "overall"
                ? `Monitoring ${userSessions.length || 1} active user account(s)`
                : `Inspecting User: ${selectedUser?.username || selectedUserId}`}
            </span>
            {userSessions.some((u) => u.mode !== "NORMAL") && (
              <span className="flex items-center gap-1 text-amber-400 font-semibold">
                <ShieldAlert className="h-3 w-3" /> User Risk Detected
              </span>
            )}
          </div>
        </div>
      </Section>

      {/* Trust Gauge */}
      <Section>
        <div className="grid place-items-center py-2">
          <TrustGauge
            score={activeGaugeScore}
            titleOverride={selectedUserId === "overall" ? "OVERALL USER AVG" : "INDIVIDUAL USER TRUST"}
          />
          <div className="mt-2 text-[10px] uppercase tracking-[0.22em] text-white/40">
            {selectedUserId === "overall" ? "System-Wide Risk Average" : "Specific User Risk Analysis"}
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