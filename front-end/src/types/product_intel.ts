// front-end/src/types/product_intel.ts
// Types for Product Intelligence features (evidence panel + priority scoring table)

export interface SourceDoc {
  /** e.g. customer_feedback | jira_tickets | support_cases | competitor_insights | usage_analytics */
  source_type: string;
  product_area: string;
  severity_or_priority: string;
  /** Truncated natural-language summary of the retrieved document */
  page_content: string;
}

export interface PriorityRow {
  product_area: string;
  frequency_score: number;
  severity_score: number;
  customer_impact_score: number;
  competitor_pressure_score: number;
  effort_score: number;
  final_score: number;
  /** "Prioritize immediately" | "Prioritize next" | "Monitor and validate" | "Defer unless strategically required" */
  recommendation: string;
}
