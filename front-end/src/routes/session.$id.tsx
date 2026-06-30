import { createFileRoute } from "@tanstack/react-router";
import { ChatView } from "@/components/Chat/ChatView";

export const Route = createFileRoute("/session/$id")({
  head: () => ({
    meta: [{ title: "AEGIS — Session" }],
  }),
  component: SessionRoute,
});

function SessionRoute() {
  const { id } = Route.useParams();
  return <ChatView key={id} sessionId={id} />;
}