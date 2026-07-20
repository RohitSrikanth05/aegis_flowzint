import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { motion } from "framer-motion";
import { ShieldCheck, Lock, User, KeyRound, AlertCircle } from "lucide-react";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "AEGIS — Login" },
      { name: "description", content: "Sign in to access AEGIS." },
    ],
  }),
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const { login, isAuthenticated, isAdmin } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  // If already logged in, redirect
  if (isAuthenticated) {
    navigate({ to: isAdmin ? "/admin" : "/" });
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const result = login(username, password);
    if (result.ok) {
      const u = username.trim().toLowerCase();
      if (u === "admin") {
        navigate({ to: "/admin" });
      } else {
        navigate({ to: "/" });
      }
    } else {
      setError(result.error || "Login failed");
    }
  };

  const fillCredentials = (acct: "admin" | "user" | "usera" | "userb") => {
    if (acct === "admin") {
      setUsername("admin");
      setPassword("admin123");
    } else if (acct === "usera") {
      setUsername("userA");
      setPassword("userA123");
    } else if (acct === "userb") {
      setUsername("userB");
      setPassword("userB123");
    } else {
      setUsername("user");
      setPassword("user123");
    }
    setError(null);
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-[#09090b] font-sans text-white px-4">
      {/* Background ambient glows */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-40 top-10 h-[420px] w-[420px] rounded-full bg-indigo-600/20 blur-[140px]" />
        <div className="absolute right-0 top-1/3 h-[420px] w-[420px] rounded-full bg-cyan-500/15 blur-[140px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 w-full max-w-md rounded-3xl border border-white/10 bg-white/[0.03] p-8 shadow-2xl backdrop-blur-xl"
      >
        <div className="flex flex-col items-center text-center">
          <div className="relative mb-4 grid h-14 w-14 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500/30 to-cyan-400/20 ring-1 ring-white/10">
            <ShieldCheck className="h-7 w-7 text-cyan-300" />
            <div className="absolute inset-0 rounded-2xl bg-cyan-400/10 blur-xl" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">AEGIS Authentication</h1>
          <p className="mt-1 text-xs text-white/50">
            Sign in to access Adaptive Enterprise Guardian Intelligence System
          </p>
        </div>

        {error && (
          <div className="mt-6 flex items-center gap-2 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-xs text-rose-300">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label className="mb-1.5 block text-[10px] font-semibold uppercase tracking-[0.18em] text-white/60">
              Username
            </label>
            <div className="relative">
              <User className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-white/30" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin or user"
                required
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2.5 pl-10 pr-4 text-sm text-white placeholder-white/20 outline-none transition focus:border-cyan-400/50 focus:bg-white/[0.06]"
              />
            </div>
          </div>

          <div>
            <label className="mb-1.5 block text-[10px] font-semibold uppercase tracking-[0.18em] text-white/60">
              Password
            </label>
            <div className="relative">
              <KeyRound className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-white/30" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                required
                className="w-full rounded-xl border border-white/10 bg-white/[0.04] py-2.5 pl-10 pr-4 text-sm text-white placeholder-white/20 outline-none transition focus:border-cyan-400/50 focus:bg-white/[0.06]"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full rounded-xl bg-gradient-to-r from-indigo-500 to-cyan-500 py-3 text-xs font-bold uppercase tracking-[0.2em] text-white transition hover:opacity-90 active:scale-[0.99]"
          >
            Sign In
          </button>
        </form>

        {/* Quick Demo Accounts */}
        <div className="mt-8 border-t border-white/10 pt-5 text-center">
          <div className="text-[10px] font-semibold uppercase tracking-[0.18em] text-white/40 mb-3">
            Quick Fill Demo Accounts
          </div>
          <div className="flex flex-wrap justify-center gap-2">
            <button
              type="button"
              onClick={() => fillCredentials("admin")}
              className="flex items-center gap-1.5 rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-1.5 text-xs text-amber-300 transition hover:bg-amber-500/20"
            >
              <Lock className="h-3 w-3" />
              Admin
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("usera")}
              className="flex items-center gap-1.5 rounded-lg border border-cyan-500/30 bg-cyan-500/10 px-3 py-1.5 text-xs text-cyan-300 transition hover:bg-cyan-500/20"
            >
              <User className="h-3 w-3" />
              User A
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("userb")}
              className="flex items-center gap-1.5 rounded-lg border border-indigo-500/30 bg-indigo-500/10 px-3 py-1.5 text-xs text-indigo-300 transition hover:bg-indigo-500/20"
            >
              <User className="h-3 w-3" />
              User B
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("user")}
              className="flex items-center gap-1.5 rounded-lg border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs text-white/70 transition hover:bg-white/[0.08]"
            >
              <User className="h-3 w-3" />
              Default User
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
