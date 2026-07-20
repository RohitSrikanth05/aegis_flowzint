export type ActivityKind = "info" | "warn" | "alert" | "learn" | "ok" | "intel";

export interface ActivityEvent {
  id: string;
  kind: ActivityKind;
  time: string;
  label: string;
}