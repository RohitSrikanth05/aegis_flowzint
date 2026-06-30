export type ChatRole = "user" | "bot";
export type ChatTone = "normal" | "alert" | "info";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  tone?: ChatTone;
  timestamp: string;
  // Live backend fields (optional, only on bot messages)
  intent?: string;
  trustScore?: number;
  confidenceScore?: number;
  mode?: string;
}