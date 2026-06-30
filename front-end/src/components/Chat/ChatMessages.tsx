import { useEffect, useRef, useState } from "react";
import { AnimatePresence } from "framer-motion";
import type { ChatMessage } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";

export function ChatMessages({ messages, typing }: { messages: ChatMessage[]; typing: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState<ChatMessage[]>([]);

  useEffect(() => {
    setVisible([]);
    let i = 0;
    const id = setInterval(() => {
      i += 1;
      setVisible(messages.slice(0, i));
      if (i >= messages.length) clearInterval(id);
    }, 600);
    return () => clearInterval(id);
  }, [messages]);

  useEffect(() => {
    ref.current?.scrollTo({ top: ref.current.scrollHeight, behavior: "smooth" });
  }, [visible, typing]);

  return (
    <div
      ref={ref}
      className="flex-1 space-y-4 overflow-y-auto px-6 py-6 [scrollbar-width:thin]"
    >
      <AnimatePresence initial={false}>
        {visible.map((m) => (
          <MessageBubble key={m.id} msg={m} />
        ))}
      </AnimatePresence>
      {typing && <TypingIndicator />}
    </div>
  );
}