import { motion } from "framer-motion";
import { Shield, AlertTriangle } from "lucide-react";
import type { ChatMessage } from "@/types/chat";
import { EvidencePanel } from "@/components/ProductIntel/EvidencePanel";
import { PriorityTable } from "@/components/ProductIntel/PriorityTable";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

// Clean up messy LLM markdown table output (e.g. TSV tabs, joined "| |", or duplicate separators)
function cleanMarkdownText(text: string): string {
  if (!text) return "";

  // 1. Pre-split joined header/separator lines (handles both `| | :---` and `| | ---` and `| |-------`)
  const preCleanedText = text.replace(/\|\s*\|\s*:?-+/g, "|\n|---");

  const lines = preCleanedText.split("\n");
  const cleanedLines: string[] = [];
  let inTable = false;
  let headerColCount = 0;
  let hasSeparator = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    if (!line) {
      inTable = false;
      hasSeparator = false;
      cleanedLines.push("");
      continue;
    }

    // Check if alignment separator line (e.g. | :--- | or :------- or |------- or --------)
    // Matches lines that start with optional | or :, followed by optional spaces/colon, and at least 3 dashes
    const isSeparatorLine = /^[|:-]?\s*:?-{3,}/.test(line);

    // Check if header row (starts with | and has multiple columns, and is NOT a separator line)
    if (line.startsWith("|") && line.split("|").length >= 4 && !isSeparatorLine) {
      const cols = line.split("|").map((c) => c.trim()).filter((c) => c.length > 0);
      if (cols.length >= 2) {
        headerColCount = cols.length;
        inTable = true;
        hasSeparator = false;
        cleanedLines.push(`| ${cols.join(" | ")} |`);
        continue;
      }
    }

    // Process separator lines
    if (isSeparatorLine) {
      if (!hasSeparator) {
        const colCount = Math.max(headerColCount, 2);
        const sep = Array(colCount).fill(":----------------").join(" | ");
        cleanedLines.push(`| ${sep} |`);
        hasSeparator = true;
        inTable = true;
      }
      continue;
    }

    // If line has tab-separated values (TSV table row)
    if (line.includes("\t")) {
      const rawCells = line.split("\t").map((c) => c.trim().replace(/^\||\|$/g, "").trim());
      const cells = rawCells.filter((c, idx) => c.length > 0 || idx < rawCells.length - 1);

      if (cells.length >= 2) {
        inTable = true;
        // Pad cells to headerColCount if header was established
        if (headerColCount > 0 && cells.length < headerColCount) {
          while (cells.length < headerColCount) cells.push("");
        }
        cleanedLines.push(`| ${cells.join(" | ")} |`);
        continue;
      }
    }

    cleanedLines.push(line);
  }

  return cleanedLines.join("\n");
}

// Custom markdown components for dark glassmorphic styling
const markdownComponents = {
  p: ({ children }: any) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
  strong: ({ children }: any) => <strong className="font-semibold text-cyan-200">{children}</strong>,
  ul: ({ children }: any) => <ul className="my-2 space-y-1 pl-4 list-disc list-outside marker:text-cyan-400/70">{children}</ul>,
  ol: ({ children }: any) => <ol className="my-2 space-y-1 pl-4 list-decimal list-outside marker:text-cyan-400/70">{children}</ol>,
  li: ({ children }: any) => <li className="pl-1 leading-relaxed">{children}</li>,
  h1: ({ children }: any) => <h1 className="mt-3 mb-1 text-base font-bold text-cyan-300">{children}</h1>,
  h2: ({ children }: any) => <h2 className="mt-3 mb-1 text-sm font-bold text-cyan-300">{children}</h2>,
  h3: ({ children }: any) => <h3 className="mt-2 mb-1 text-xs font-bold uppercase tracking-wider text-cyan-300/90">{children}</h3>,
  code: ({ children }: any) => (
    <code className="rounded bg-black/40 px-1.5 py-0.5 font-mono text-xs text-cyan-300 border border-white/10">
      {children}
    </code>
  ),
  table: ({ children }: any) => (
    <div className="my-3 overflow-x-auto rounded-xl border border-white/10 bg-black/30 shadow-lg">
      <table className="w-full text-left text-xs border-collapse">{children}</table>
    </div>
  ),
  thead: ({ children }: any) => (
    <thead className="bg-white/[0.08] text-cyan-300 font-semibold uppercase tracking-wider border-b border-white/10">
      {children}
    </thead>
  ),
  tbody: ({ children }: any) => <tbody className="divide-y divide-white/5">{children}</tbody>,
  tr: ({ children }: any) => <tr className="hover:bg-white/[0.04] transition-colors">{children}</tr>,
  th: ({ children }: any) => <th className="px-3 py-2 font-semibold text-cyan-200">{children}</th>,
  td: ({ children }: any) => <td className="px-3 py-2 text-white/85">{children}</td>,
};

export function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === "user";
  const isAlert = msg.tone === "alert";
  const hasEvidence = !isUser && msg.sources && msg.sources.length > 0;
  const hasPriorityTable = !isUser && msg.priorityTable && msg.priorityTable.length > 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div className={`flex max-w-[85%] gap-2 ${isUser ? "flex-row-reverse" : ""}`}>
        {!isUser && (
          <div className="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-gradient-to-br from-indigo-500/40 to-cyan-400/30 ring-1 ring-white/10">
            <Shield className="h-3.5 w-3.5 text-cyan-200" />
          </div>
        )}
        <div className="flex-1 min-w-0">
          <div
            className={[
              "rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-lg transition-transform hover:scale-[1.005]",
              isUser
                ? "bg-white/[0.06] text-white/90 ring-1 ring-white/10"
                : isAlert
                  ? "bg-gradient-to-br from-rose-500/25 to-amber-500/15 text-rose-50 ring-1 ring-rose-400/30"
                  : "bg-gradient-to-br from-indigo-500/30 via-violet-500/20 to-cyan-400/20 text-white ring-1 ring-white/10",
            ].join(" ")}
          >
            {isAlert && (
              <div className="mb-1.5 flex items-center gap-1.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-rose-300">
                <AlertTriangle className="h-3 w-3" /> Security Notice
              </div>
            )}

            {isUser ? (
              <div className="whitespace-pre-wrap">{msg.content}</div>
            ) : (
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
                {cleanMarkdownText(msg.content)}
              </ReactMarkdown>
            )}

            <div className="mt-1.5 text-[10px] uppercase tracking-wider text-white/30">
              {msg.timestamp}
            </div>
          </div>

          {/* Product Intelligence — Evidence Panel */}
          {hasEvidence && <EvidencePanel sources={msg.sources!} />}

          {/* Product Intelligence — Priority Score Table */}
          {hasPriorityTable && <PriorityTable rows={msg.priorityTable!} />}
        </div>
      </div>
    </motion.div>
  );
}