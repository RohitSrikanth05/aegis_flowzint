import { createFileRoute } from "@tanstack/react-router";
import { ChatView } from "@/components/Chat/ChatView";

export const Route = createFileRoute("/admin")({
  head: () => ({
    meta: [
      { title: "AEGIS — Admin View" },
      {
        name: "description",
        content:
          "Admin view: full trust cockpit, security center, and knowledge learning queue.",
      },
    ],
  }),
  component: AdminIndex,
});

import { useAuth } from "@/hooks/useAuth";
import { useEffect } from "react";
import { useNavigate } from "@tanstack/react-router";

function AdminIndex() {
  const { isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate({ to: "/login" });
    } else if (!isAdmin) {
      navigate({ to: "/" });
    }
  }, [isAuthenticated, isAdmin, navigate]);

  if (!isAuthenticated || !isAdmin) return null;

  return <ChatView isAdmin={true} />;
}
