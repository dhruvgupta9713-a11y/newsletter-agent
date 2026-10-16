export interface SystemStatus {
  demo_mode: boolean;
  openai_configured: boolean;
  openai_model: string;
  tavily_configured: boolean;
  search_provider: string;
  output_directory: string;
  default_subscribers: number;
  status: string;
}

export interface Article {
  title: string;
  url: string;
  source: string;
  snippet: string;
  published_date?: string;
  score?: number;
  approved?: boolean;
}

export interface ArticleSummary {
  title: string;
  source: string;
  published_date: string;
  summary: string;
  why_it_matters: string;
  key_takeaway: string;
  url: string;
}

export interface PlanData {
  topic: string;
  audience: string;
  time_range: string;
  target_article_count: number;
  search_queries: string[];
  execution_steps: string[];
}

export interface CritiqueData {
  quality_score: number;
  is_valid: boolean;
  issues: string[];
  suggestions: string[];
  deterministic_checks: {
    article_count_valid: boolean;
    article_count: number;
    has_subject_line: boolean;
    has_html_content: boolean;
    has_markdown_content: boolean;
    all_urls_valid: boolean;
    urls_verified_count: number;
  };
}

export interface DeliveryData {
  simulated: boolean;
  recipient_count: number;
  timestamp: string;
  status: string;
  subscribers_sample: string[];
  label?: string;
  notice: string;
}

export interface ActivityLogEntry {
  timestamp: string;
  step: string;
  tool_name: string;
  description: string;
  status: 'success' | 'warning' | 'error' | 'running';
  details?: any;
}

export interface AgentRunState {
  run_id: string;
  goal: string;
  mode: 'autonomous' | 'hitl';
  plan?: PlanData | null;
  search_queries: string[];
  raw_articles: Article[];
  selected_articles: Article[];
  research_approved: boolean;
  summaries: ArticleSummary[];
  newsletter_title: string;
  subject_line: string;
  newsletter_html: string;
  newsletter_markdown: string;
  newsletter_approved: boolean;
  critique?: CritiqueData | null;
  revision_count: number;
  revision_feedback?: string | null;
  simulated_delivery?: DeliveryData | null;
  output_files: {
    html_filename?: string;
    md_filename?: string;
    json_filename?: string;
    html_path?: string;
    md_path?: string;
    json_path?: string;
  };
  logs: ActivityLogEntry[];
  current_step: string;
  status: 
    | 'planning'
    | 'researching'
    | 'waiting_research_approval'
    | 'summarizing'
    | 'writing'
    | 'critiquing'
    | 'revising'
    | 'waiting_newsletter_approval'
    | 'sending'
    | 'completed'
    | 'failed'
    | 'rejected';
  error?: string | null;
  duration_seconds: number;
}
