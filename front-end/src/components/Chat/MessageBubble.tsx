import { motion } from "framer-motion";
import { Shield, AlertTriangle } from "lucide-react";
import type { ChatMessage } from "@/types/chat";

export function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === "user";
  const isAlert = msg.tone === "alert";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div className={`flex max-w-[78%] gap-2 ${isUser ? "flex-row-reverse" : ""}`}>
        {!isUser && (
          <div className="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-gradient-to-br from-indigo-500/40 to-cyan-400/30 ring-1 ring-white/10">
            <Shield className="h-3.5 w-3.5 text-cyan-200" />
          </div>
        )}
        <div
          className={[
            "rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-lg transition-transform hover:scale-[1.01]",
            isUser
              ? "bg-white/[0.06] text-white/90 ring-1 ring-white/10"
              : isAlert
                ? "bg-gradient-to-br from-rose-500/25 to-amber-500/15 text-rose-50 ring-1 ring-rose-400/30"
                : "bg-gradient-to-br from-indigo-500/30 via-violet-500/20 to-cyan-400/20 text-white ring-1 ring-white/10",
          ].join(" ")}
        >
          {isAlert && (
            <div className="mb-1.5 flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-rose-300">
              <AlertTriangle className="h-3 w-3" /> Security Notice
            </div>
          )}
          <div>{msg.content}</div>
          <div className="mt-1.5 text-[10px] uppercase tracking-wider text-white/30">
            {msg.timestamp}
          </div>
        </div>
      </div>
    </motion.div>
  );
}