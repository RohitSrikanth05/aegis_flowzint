export type Mode = "sales" | "support" | "care";

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