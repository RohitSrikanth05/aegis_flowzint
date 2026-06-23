import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { ScrollArea } from "@/components/ui/scroll-area";
import { History, MessageSquare, Plus, Trash2, Shield } from "lucide-react";
import { useNavigate } from "@tanstack/react-router";
import { useSessions } from "@/hooks/useSessions";
import { motion } from "framer-motion";
import { useState } from "react";

function timeAgo(ts: number) {
  const s = Math.floor((Date.now() - ts) / 1000);
  if (s < 60) return `${s}s ago`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  const d = Math.floor(h / 24);
  return `${d}d ago`;
}

export function SessionsSheet({ activeId }: { activeId?: string }) {
  const navigate = useNavigate();
  const { sessions, remove, clear } = useSessions();
  const [open, setOpen] = useState(false);

  const go = (id: string) => {
    setOpen(false);
    navigate({ to: "/session/$id", params: { id } });
  };

  const newSession = () => {
    setOpen(false);
    navigate({ to: "/" });
  };

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <button className="inline-flex items-center gap-2 rounded-lg border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs font-medium text-white/70 transition hover:border-cyan-400/30 hover:bg-white/[0.06] hover:text-white">
          <History className="h-3.5 w-3.5" />
          Sessions
          {sessions.length > 0 && (
            <span className="rounded-md bg-cyan-400/10 px-1.5 py-0.5 text-[10px] font-semibold text-cyan-300">
              {sessions.length}
            </span>
          )}
        </button>
      </SheetTrigger>
      <SheetContent
        side="left"
        className="w-[340px] border-r border-white/10 bg-[#0b0b10] p-0 text-white sm:w-[380px]"
      >
        <SheetHeader className="border-b border-white/10 px-5 py-4">
          <SheetTitle className="flex items-center gap-2 text-white">
            <div className="grid h-8 w-8 place-items-center rounded-lg bg-gradient-to-br from-indigo-500/30 to-cyan-400/20 ring-1 ring-white/10">
              <Shield className="h-4 w-4 text-cyan-300" />
            </div>
            <div>
              <div className="text-sm font-semibold">Session History</div>
              <div className="text-[10px] font-normal uppercase tracking-[0.18em] text-white/40">
                Encrypted · Local Vault
              </div>
            </div>
          </SheetTitle>
        </SheetHeader>

        <div className="flex items-center gap-2 border-b border-white/10 px-5 py-3">
          <button
            onClick={newSession}
            className="inline-flex flex-1 items-center justify-center gap-2 rounded-lg bg-gradient-to-br from-indigo-500 to-cyan-400 px-3 py-2 text-xs font-semibold text-white shadow-[0_6px_24px_rgba(56,189,248,0.35)] transition hover:brightness-110"
          >
            <Plus className="h-3.5 w-3.5" /> New session
          </button>
          {sessions.length > 0 && (
            <button
              onClick={clear}
              className="rounded-lg border border-white/10 p-2 text-white/40 transition hover:border-red-400/30 hover:text-red-300"
              title="Clear all"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </button>
          )}
        </div>

        <ScrollArea className="h-[calc(100vh-148px)]">
          <div className="space-y-1 p-3">
            {sessions.length === 0 && (
              <div className="px-3 py-12 text-center">
                <div className="mx-auto mb-3 grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-white/[0.03]">
                  <MessageSquare className="h-4 w-4 text-white/40" />
                </div>
                <div className="text-xs font-medium text-white/60">No previous sessions</div>
                <div className="mt-1 text-[10px] text-white/30">
                  Your conversations will appear here
                </div>
              </div>
            )}
            {sessions.map((s, i) => {
              const isActive = s.id === activeId;
              return (
                <motion.div
                  key={s.id}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.02 }}
                  className={`group flex items-center gap-2 rounded-lg border px-3 py-2.5 transition ${
                    isActive
                      ? "border-cyan-400/40 bg-cyan-400/[0.06]"
                      : "border-white/[0.06] bg-white/[0.02] hover:border-white/15 hover:bg-white/[0.04]"
                  }`}
                >
                  <button
                    onClick={() => go(s.id)}
                    className="flex min-w-0 flex-1 items-center gap-3 text-left"
                  >
                    <div
                      className={`grid h-7 w-7 shrink-0 place-items-center rounded-md ${
                        isActive
                          ? "bg-cyan-400/15 text-cyan-300"
                          : "bg-white/5 text-white/50 group-hover:text-white/80"
                      }`}
                    >
                      <MessageSquare className="h-3.5 w-3.5" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="truncate text-xs font-medium text-white/90">{s.title}</div>
                      <div className="mt-0.5 flex items-center gap-1.5 text-[10px] text-white/40">
                        <span>{s.messages.length} msg</span>
                        <span className="h-0.5 w-0.5 rounded-full bg-white/20" />
                        <span>{timeAgo(s.updatedAt)}</span>
                      </div>
                    </div>
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      remove(s.id);
                    }}
                    className="rounded p-1 text-white/30 opacity-0 transition hover:bg-red-500/10 hover:text-red-300 group-hover:opacity-100"
                    title="Delete"
                  >
                    <Trash2 className="h-3 w-3" />
                  </button>
                </motion.div>
              );
            })}
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}