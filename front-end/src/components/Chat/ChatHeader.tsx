import { Shield, Lock, LogOut, User } from "lucide-react";
import { motion } from "framer-motion";
import { SessionsSheet } from "./SessionsSheet";
import { useAuth } from "@/hooks/useAuth";
import { useNavigate } from "@tanstack/react-router";

export function ChatHeader({
  sessionId,
  sessionLabel,
  isAdmin = false,
}: {
  sessionId?: string;
  sessionLabel?: string;
  isAdmin?: boolean;
}) {
  const { username, logout, isAdmin: authIsAdmin } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate({ to: "/login" });
  };

  return (
    <div className="flex items-center justify-between border-b border-[var(--color-aegis-border)] px-6 py-4">
      <div className="flex min-w-0 items-center gap-3">
        <SessionsSheet activeId={sessionId} />
        <div className="relative grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-indigo-500/30 to-cyan-400/20 ring-1 ring-white/10">
          <Shield className="h-5 w-5 text-cyan-300" />
          <div className="absolute inset-0 rounded-xl bg-cyan-400/10 blur-xl" />
        </div>
        <div className="min-w-0">
          <div className="text-base font-bold tracking-wide text-white">AEGIS</div>
          <div className="truncate text-[10px] uppercase tracking-[0.18em] text-white/40">
            {sessionLabel ?? "Adaptive Enterprise Guardian Intelligence System"}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {isAdmin ? (
          /* Admin mode badge */
          <div className="flex items-center gap-2">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1.5"
            >
              <Lock className="h-3 w-3 text-amber-400" />
              <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-amber-300">
                Admin Mode
              </span>
            </motion.div>
            <a
              href="/"
              className="text-[10px] font-semibold uppercase tracking-[0.15em] text-white/40 transition hover:text-white"
            >
              User View →
            </a>
          </div>
        ) : (
          /* User view — if admin user, show link to admin view */
          authIsAdmin && (
            <a
              href="/admin"
              className="text-[10px] font-semibold uppercase tracking-[0.15em] text-white/40 transition hover:text-white"
            >
              Admin Cockpit →
            </a>
          )
        )}

        {/* User Badge */}
        {username && (
          <div className="flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-[10px] font-medium text-white/70">
            <User className="h-3 w-3 text-cyan-400" />
            <span className="capitalize">{username}</span>
          </div>
        )}

        {/* Live indicator */}
        <div className="flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5">
          <span className="relative flex h-2 w-2">
            <motion.span
              className="absolute inline-flex h-full w-full rounded-full bg-emerald-400"
              animate={{ opacity: [0.4, 1, 0.4], scale: [1, 1.6, 1] }}
              transition={{ duration: 1.8, repeat: Infinity }}
            />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
          </span>
          <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-emerald-300">
            {isAdmin ? "Admin · Live" : "Secure Session"}
          </span>
        </div>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          title="Sign out"
          className="flex items-center gap-1 rounded-full border border-white/10 bg-white/[0.03] p-1.5 text-white/40 transition hover:border-rose-500/30 hover:bg-rose-500/10 hover:text-rose-300"
        >
          <LogOut className="h-3.5 w-3.5" />
        </button>
      </div>
    </div>
  );
}