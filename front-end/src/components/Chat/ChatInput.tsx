import { Paperclip, Mic, ArrowUp } from "lucide-react";
import { motion } from "framer-motion";
import { useState } from "react";

export function ChatInput({ onSend }: { onSend: (text: string) => void }) {
  const [value, setValue] = useState("");
  const submit = () => {
    const v = value.trim();
    if (!v) return;
    onSend(v);
    setValue("");
  };
  return (
    <div className="border-t border-[var(--color-aegis-border)] bg-black/30 px-6 py-4 backdrop-blur">
      <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/[0.04] px-3 py-2 shadow-[0_8px_30px_rgba(0,0,0,0.35)] focus-within:border-cyan-400/30 focus-within:shadow-[0_0_0_3px_rgba(34,211,238,0.08)]">
        <button className="rounded-lg p-2 text-white/40 transition hover:bg-white/5 hover:text-white/70">
          <Paperclip className="h-4 w-4" />
        </button>
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="Ask anything…"
          className="flex-1 bg-transparent px-1 py-2 text-sm text-white placeholder:text-white/30 focus:outline-none"
        />
        <button className="rounded-lg p-2 text-white/40 transition hover:bg-white/5 hover:text-white/70">
          <Mic className="h-4 w-4" />
        </button>
        <motion.button
          whileHover={{ scale: 1.06 }}
          whileTap={{ scale: 0.94 }}
          onClick={submit}
          className="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-indigo-500 to-cyan-400 text-white shadow-[0_6px_24px_rgba(56,189,248,0.45)]"
        >
          <ArrowUp className="h-4 w-4" />
        </motion.button>
      </div>
      <div className="mt-2 px-2 text-[10px] uppercase tracking-[0.18em] text-white/30">
        End-to-end inspected · Trust engine active
      </div>
    </div>
  );
}