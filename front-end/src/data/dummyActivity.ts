import type { ActivityEvent } from "@/types/activity";
import type { SecurityEvent, LearningItem } from "@/types/trust";

export const dummyActivity: ActivityEvent[] = [
  { id: "a1", kind: "ok", time: "8:31 PM", label: "Sales Intent Detected" },
  { id: "a2", kind: "warn", time: "8:32 PM", label: "Refund Request Processing" },
  { id: "a3", kind: "alert", time: "8:33 PM", label: "Manipulation Attempt Detected" },
  { id: "a4", kind: "info", time: "8:34 PM", label: "Knowledge Gap Identified" },
  { id: "a5", kind: "learn", time: "8:35 PM", label: "Learning Request Queued" },
];

export const dummySecurity: SecurityEvent[] = [
  { id: "s1", label: "Prompt Injection Attempt", severity: "high", status: "Blocked" },
  { id: "s2", label: "Policy Override Request", severity: "medium", status: "Denied" },
  { id: "s3", label: "Refund Fraud Attempt", severity: "critical", status: "Escalated" },
  { id: "s4", label: "Jailbreak Attack", severity: "high", status: "Blocked" },
];

export const dummyLearning: LearningItem = {
  id: "l1",
  question: "What is the warranty on Product X?",
  status: "Pending Review",
};