import React, { useState, useEffect, useRef } from 'react';
import { Header } from './components/Header';
import { AgentConfig } from './components/AgentConfig';
import { ExecutionTimeline } from './components/ExecutionTimeline';
import { ResearchResults } from './components/ResearchResults';
import { AgentActivityLog } from './components/AgentActivityLog';
import { NewsletterPreview } from './components/NewsletterPreview';
import { FinalReport } from './components/FinalReport';
import { 
  fetchSystemStatus, 
  runAgentWorkflow, 
  fetchAgentState, 
  approveResearchPhase, 
  approveNewsletterDraft, 
  requestRevision 
} from './api';
import type { AgentRunState, SystemStatus, Article } from './types';
import { AlertCircle, Bot, Sparkles } from 'lucide-react';

export const App: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [runState, setRunState] = useState<AgentRunState | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Poll interval ref
  const pollTimerRef = useRef<any>(null);

  // Load system status on mount
  useEffect(() => {
    fetchSystemStatus()
      .then(status => setSystemStatus(status))
      .catch(err => {
        console.warn('Failed to fetch system status:', err);
      });

    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current);
    };
  }, []);

  // Poll state if in-progress
  const startPolling = (runId: string) => {
    if (pollTimerRef.current) clearInterval(pollTimerRef.current);

    pollTimerRef.current = setInterval(async () => {
      try {
        const state = await fetchAgentState(runId);
        setRunState(state);

        if (
          state.status === 'completed' ||
          state.status === 'waiting_research_approval' ||
          state.status === 'waiting_newsletter_approval' ||
          state.status === 'failed'
        ) {
          if (pollTimerRef.current) {
            clearInterval(pollTimerRef.current);
            pollTimerRef.current = null;
          }
          setIsLoading(false);
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    }, 1000);
  };

  const handleRunAgent = async (goal: string, mode: 'autonomous' | 'hitl', articleCount: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const res = await runAgentWorkflow(goal, mode, articleCount);
      setRunState(res.state);

      if (
        res.state.status !== 'completed' &&
        res.state.status !== 'waiting_research_approval' &&
        res.state.status !== 'waiting_newsletter_approval'
      ) {
        startPolling(res.run_id);
      } else {
        setIsLoading(false);
      }
    } catch (err: any) {
      setError(err.message || 'Execution failed');
      setIsLoading(false);
    }
  };

  const handleApproveResearch = async (approvedArticles: Article[]) => {
    if (!runState) return;
    setIsLoading(true);
    setError(null);

    try {
      const res = await approveResearchPhase(runState.run_id, approvedArticles);
      setRunState(res.state);

      if (
        res.state.status !== 'completed' &&
        res.state.status !== 'waiting_newsletter_approval'
      ) {
        startPolling(res.run_id);
      } else {
        setIsLoading(false);
      }
    } catch (err: any) {
      setError(err.message || 'Research approval failed');
      setIsLoading(false);
    }
  };

  const handleApproveNewsletter = async () => {
    if (!runState) return;
    setIsLoading(true);
    setError(null);

    try {
      const res = await approveNewsletterDraft(runState.run_id);
      setRunState(res.state);
      setIsLoading(false);
    } catch (err: any) {
      setError(err.message || 'Newsletter approval failed');
      setIsLoading(false);
    }
  };

  const handleRequestRevision = async (feedback: string) => {
    if (!runState) return;
    setIsLoading(true);
    setError(null);

    try {
      const res = await requestRevision(runState.run_id, feedback);
      setRunState(res.state);
      setIsLoading(false);
    } catch (err: any) {
      setError(err.message || 'Revision request failed');
      setIsLoading(false);
    }
  };

  const hasDraft = Boolean(runState?.newsletter_html || runState?.newsletter_markdown);
  const isCompleted = runState?.status === 'completed';

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Header */}
      <Header status={systemStatus} loading={isLoading} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Error notification */}
        {error && (
          <div className="bg-rose-500/10 border border-rose-500/30 p-4 rounded-xl flex items-center justify-between text-rose-300 text-sm">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-xs bg-rose-950/50 hover:bg-rose-900/50 px-2 py-1 rounded border border-rose-800"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Top Control Section: Configuration */}
        <section>
          <AgentConfig
            onRun={handleRunAgent}
            isLoading={isLoading}
            activeStatus={runState?.status}
          />
        </section>

        {/* Execution Timeline */}
        {runState && (
          <section>
            <ExecutionTimeline state={runState} isLoading={isLoading} />
          </section>
        )}

        {/* Final Report (Shown when completed) */}
        {isCompleted && runState && (
          <section>
            <FinalReport state={runState} />
          </section>
        )}

        {/* Workspace Display Grid */}
        {runState && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left Column: Newsletter Preview & Research Results (7 cols on large) */}
            <div className="lg:col-span-7 space-y-8">
              {/* Newsletter Preview */}
              {hasDraft && (
                <section>
                  <NewsletterPreview
                    state={runState}
                    onApproveNewsletter={handleApproveNewsletter}
                    onRequestRevision={handleRequestRevision}
                    isLoading={isLoading}
                  />
                </section>
              )}

              {/* Research Results */}
              <section>
                <ResearchResults
                  state={runState}
                  onApproveResearch={handleApproveResearch}
                  isLoading={isLoading}
                />
              </section>
            </div>

            {/* Right Column: Agent Activity Log & Reflection (5 cols on large) */}
            <div className="lg:col-span-5 space-y-8">
              <section>
                <AgentActivityLog
                  logs={runState.logs || []}
                  critique={runState.critique}
                  revisionCount={runState.revision_count}
                />
              </section>
            </div>
          </div>
        )}

        {/* Welcome Empty State if no run yet */}
        {!runState && (
          <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-12 text-center max-w-2xl mx-auto my-12">
            <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto mb-4">
              <Bot className="w-7 h-7" />
            </div>
            <h2 className="text-xl font-bold text-white mb-2">Autonomous AI Newsletter Engine</h2>
            <p className="text-slate-400 text-sm leading-relaxed mb-6">
              Enter your natural language objective above and select your preferred autonomy mode.
              The agent will independently research latest AI developments, deduplicate canonical sources,
              synthesize high-density technical summaries, conduct self-critique, and simulate subscriber dispatch.
            </p>
            <div className="grid grid-cols-3 gap-3 text-left text-xs bg-slate-950/60 p-4 rounded-xl border border-slate-800">
              <div>
                <span className="font-semibold text-sky-400 block mb-1">1. Research</span>
                <span className="text-slate-400">Queries Tavily or curated AI intelligence for 5-7 verified stories.</span>
              </div>
              <div>
                <span className="font-semibold text-indigo-400 block mb-1">2. Self-Review</span>
                <span className="text-slate-400">Scores quality out of 100 with deterministic URL & field validation.</span>
              </div>
              <div>
                <span className="font-semibold text-emerald-400 block mb-1">3. Simulated Send</span>
                <span className="text-slate-400">Generates responsive HTML/Markdown files without sending real email.</span>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/60 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span>Autonomous AI Newsletter Agent &bull; LangGraph &bull; FastAPI &bull; React Vite</span>
          </div>
          <div>
            <span>NOTICE: All newsletter dispatches are <strong>SIMULATED</strong>. No external emails are sent.</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
