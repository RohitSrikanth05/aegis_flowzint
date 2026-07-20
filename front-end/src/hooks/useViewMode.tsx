// front-end/src/hooks/useViewMode.tsx
// Tracks whether we are in "user" or "admin" view.
// Admin view is determined by the URL prefix /admin — no auth required.

import { createContext, useContext, useMemo, type ReactNode } from "react";
import { useRouterState } from "@tanstack/react-router";

type ViewMode = "user" | "admin";

const ViewModeContext = createContext<ViewMode>("user");

export function ViewModeProvider({ children }: { children: ReactNode }) {
  const routerState = useRouterState();
  const pathname = routerState.location.pathname;
  const mode: ViewMode = pathname.startsWith("/admin") ? "admin" : "user";

  return (
    <ViewModeContext.Provider value={mode}>{children}</ViewModeContext.Provider>
  );
}

export function useViewMode(): ViewMode {
  return useContext(ViewModeContext);
}
