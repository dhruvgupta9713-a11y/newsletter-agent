import type { AgentRunState, SystemStatus, Article } from './types';

const API_PREFIX = (import.meta as any).env?.VITE_API_URL || '';
const API_BASE = `${API_PREFIX}/api/agent`;

export async function fetchSystemStatus(): Promise<SystemStatus> {
  const res = await fetch(`${API_BASE}/status`);
  if (!res.ok) {
    throw new Error(`Failed to fetch system status: ${res.statusText}`);
  }
  return res.json();
}

export async function runAgentWorkflow(
  goal: string,
  mode: 'autonomous' | 'hitl',
  targetArticleCount: number = 6
): Promise<{ run_id: string; status: string; state: AgentRunState }> {
  const res = await fetch(`${API_BASE}/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonStringify({
      goal,
      mode,
      target_article_count: targetArticleCount,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to start agent workflow');
  }
  return res.json();
}

export async function fetchAgentState(runId: string): Promise<AgentRunState> {
  const res = await fetch(`${API_BASE}/${runId}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch run state: ${res.statusText}`);
  }
  return res.json();
}

export async function approveResearchPhase(
  runId: string,
  approvedArticles: Article[]
): Promise<{ run_id: string; status: string; state: AgentRunState }> {
  const res = await fetch(`${API_BASE}/${runId}/approve-research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonStringify({ approved_articles: approvedArticles }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to approve research');
  }
  return res.json();
}

export async function approveNewsletterDraft(
  runId: string
): Promise<{ run_id: string; status: string; state: AgentRunState }> {
  const res = await fetch(`${API_BASE}/${runId}/approve-newsletter`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to approve newsletter');
  }
  return res.json();
}

export async function requestRevision(
  runId: string,
  feedback: string
): Promise<{ run_id: string; status: string; state: AgentRunState }> {
  const res = await fetch(`${API_BASE}/${runId}/revise`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: jsonStringify({ feedback }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Failed to request revision');
  }
  return res.json();
}

export function getDownloadUrl(runId: string, format: 'html' | 'md' | 'json'): string {
  return `${API_BASE}/${runId}/download/${format}`;
}

function jsonStringify(obj: any): string {
  return JSON.stringify(obj);
}
