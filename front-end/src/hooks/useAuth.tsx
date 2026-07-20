// front-end/src/hooks/useAuth.tsx
// Lightweight client-side auth context.
// Credentials are hardcoded — no backend auth required.
// Roles: "admin" | "user" | null (not logged in)

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from "react";

export type AuthRole = "admin" | "user";

interface AuthState {
  role: AuthRole | null;
  username: string | null;
}

interface AuthContextValue extends AuthState {
  login: (username: string, password: string) => { ok: boolean; error?: string };
  logout: () => void;
  isAuthenticated: boolean;
  isAdmin: boolean;
}

// ── Credentials store (hardcoded) ─────────────────────────────────────────────
const CREDENTIALS: Record<string, { password: string; role: AuthRole }> = {
  admin: { password: "admin123", role: "admin" },
  user: { password: "user123", role: "user" },
  usera: { password: "userA123", role: "user" },
  userb: { password: "userB123", role: "user" },
};

const LS_ROLE_KEY = "aegis_role";
const LS_USER_KEY = "aegis_username";

// ── Context ───────────────────────────────────────────────────────────────────
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>(() => {
    if (typeof window === "undefined") {
      return { role: null, username: null };
    }
    // Rehydrate from localStorage on client mount
    const role = localStorage.getItem(LS_ROLE_KEY) as AuthRole | null;
    const username = localStorage.getItem(LS_USER_KEY);
    return { role, username };
  });

  // Keep localStorage in sync
  useEffect(() => {
    if (typeof window === "undefined") return;
    if (state.role && state.username) {
      localStorage.setItem(LS_ROLE_KEY, state.role);
      localStorage.setItem(LS_USER_KEY, state.username);
    } else {
      localStorage.removeItem(LS_ROLE_KEY);
      localStorage.removeItem(LS_USER_KEY);
    }
  }, [state]);

  const login = useCallback(
    (username: string, password: string): { ok: boolean; error?: string } => {
      const entry = CREDENTIALS[username.trim().toLowerCase()];
      if (!entry) {
        return { ok: false, error: "Username not found." };
      }
      if (entry.password !== password) {
        return { ok: false, error: "Incorrect password." };
      }
      setState({ role: entry.role, username: username.trim().toLowerCase() });
      return { ok: true };
    },
    [],
  );

  const logout = useCallback(() => {
    setState({ role: null, username: null });
  }, []);

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        logout,
        isAuthenticated: state.role !== null,
        isAdmin: state.role === "admin",
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
