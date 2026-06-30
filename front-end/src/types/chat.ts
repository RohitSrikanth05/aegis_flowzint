export type ChatRole = "user" | "bot";
export type ChatTone = "normal" | "alert" | "info";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  tone?: ChatTone;
  timestamp: string;
}