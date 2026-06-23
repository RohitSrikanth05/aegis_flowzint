import { createFileRoute } from "@tanstack/react-router";
import { ChatView } from "@/components/Chat/ChatView";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "AEGIS — AI Security Command Center" },
      {
        name: "description",
        content:
          "Adaptive Enterprise Guardian Intelligence System. Trust scoring, manipulation detection, and self-learning customer AI.",
      },
      { property: "og:title", content: "AEGIS — AI Security Command Center" },
      {
        property: "og:description",
        content: "Trust scoring, manipulation detection, and self-learning customer AI.",
      },
    ],
  }),
  component: Index,
});

function Index() {
  return <ChatView />;
}