import { useEffect, useRef, useState } from "react";
import { AnimatePresence } from "framer-motion";
import type { ChatMessage } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";

export function ChatMessages({ messages, typing }: { messages: ChatMessage[]; typing: boolean }) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState<ChatMessage[]>([]);
  const renderedCountRef = useRef(0);

  useEffect(() => {
    if (messages.length < renderedCountRef.current) {
      renderedCountRef.current = messages.length;
      setVisible(messages);
      return;
    }

    if (messages.length === renderedCountRef.current) {
      return;
    }

    const nextMessages = messages.slice(renderedCountRef.current);
    if (nextMessages.length === 0) {
      renderedCountRef.current = messages.length;
      return;
    }

    let index = 0;
    const intervalId = setInterval(() => {
      const nextMessage = nextMessages[index];
      index += 1;
      renderedCountRef.current += 1;
      setVisible((current) => [...current, nextMessage]);
      if (index >= nextMessages.length) {
        clearInterval(intervalId);
      }
    }, 250);

    return () => clearInterval(intervalId);
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