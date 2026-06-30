// Trust mode from backend: NORMAL, CAUTIOUS, LOCKDOWN (mapped from intent: sales, support, care for display)
export type Mode = "sales" | "support" | "care";
// Backend mode values
export type TrustMode = "NORMAL" | "CAUTIOUS" | "LOCKDOWN";

export interface SecurityEvent {
  id: string;
  label: string;
  severity: "low" | "medium" | "high" | "critical";
  status: "Blocked" | "Denied" | "Escalated" | "Resolved";
}

export interface LearningItem {
  id: string;
  question: string;
  status: "Unknown" | "Pending Review" | "Approved" | "Learned";
}