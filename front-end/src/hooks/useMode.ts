import { useEffect, useState } from "react";
import type { Mode } from "@/types/trust";

const order: Mode[] = ["sales", "support", "care"];

export function useMode(initial: Mode = "sales") {
  const [mode, setMode] = useState<Mode>(initial);
  useEffect(() => {
    let i = order.indexOf(initial);
    const id = setInterval(() => {
      i = (i + 1) % order.length;
      setMode(order[i]);
    }, 6000);
    return () => clearInterval(id);
  }, [initial]);
  return mode;
}