import { createFileRoute } from "@tanstack/react-router";
import { ChatView } from "@/components/Chat/ChatView";

export const Route = createFileRoute("/session/$id")({
  head: () => ({
    meta: [{ title: "AEGIS — Session" }],
  }),
  component: SessionRoute,
});

import { useAuth } from "@/hooks/useAuth";
import { useEffect } from "react";
import { useNavigate } from "@tanstack/react-router";

function SessionRoute() {
  const { id } = Route.useParams();
  const { isAuthenticated, isAdmin } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate({ to: "/login" });
    }
  }, [isAuthenticated, navigate]);

  if (!isAuthenticated) return null;

  return <ChatView key={id} sessionId={id} isAdmin={isAdmin} />;
}