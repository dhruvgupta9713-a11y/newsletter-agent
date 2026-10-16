import React, { useState } from 'react';
import { Play, Sparkles, UserCheck, Zap, RefreshCw } from 'lucide-react';

interface AgentConfigProps {
  onRun: (goal: string, mode: 'autonomous' | 'hitl', articleCount: number) => void;
  isLoading: boolean;
  activeStatus?: string;
}

const PRESET_GOALS = [
  "Create a weekly newsletter on the latest AI agent news and send it to our subscribers.",
  "Synthesize recent breakthroughs in SWE-bench autonomous coding agents and developer tooling.",
  "Curate enterprise multi-agent orchestration frameworks, security vulnerabilities, and deployment patterns.",
  "Report on lightweight edge models for local autonomous agents including Llama 3.2 and Smolagents."
];

export const AgentConfig: React.FC<AgentConfigProps> = ({ onRun, isLoading, activeStatus }) => {
  const [goal, setGoal] = useState<string>(PRESET_GOALS[0]);
  const [mode, setMode] = useState<'autonomous' | 'hitl'>('autonomous');
  const [articleCount, setArticleCount] = useState<number>(6);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!goal.trim() || isLoading) return;
    onRun(goal, mode, articleCount);
  };

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl relative overflow-hidden backdrop-blur-sm">
      {/* Glow accent */}
      <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <div className="flex items-center justify-between mb-2">
            <label htmlFor="goal-input" className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-sky-400" />
              Agent Objective & Goal
            </label>
            <span className="text-xs text-slate-400">Natural language goal input</span>
          </div>

          <textarea
            id="goal-input"
            rows={3}
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            disabled={isLoading}
            placeholder="Describe what newsletter to create (e.g., topic, audience, scope)..."
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all shadow-inner disabled:opacity-60 resize-none"
          />

          {/* Quick presets */}
          <div className="mt-2.5 flex flex-wrap items-center gap-1.5">
            <span className="text-[11px] text-slate-400 font-medium mr-1">Suggested Goals:</span>
            {PRESET_GOALS.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setGoal(preset)}
                disabled={isLoading}
                className="text-[11px] bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700/50 transition-colors truncate max-w-[280px]"
                title={preset}
              >
                {preset.slice(0, 38)}...
              </button>
            ))}
          </div>
        </div>

        {/* Mode Selector and Controls */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          {/* Autonomy Mode */}
          <div>
            <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">
              Autonomy Level
            </label>
            <div className="grid grid-cols-2 gap-2 bg-slate-950/70 p-1.5 rounded-xl border border-slate-800">
              <button
                type="button"
                onClick={() => setMode('autonomous')}
                disabled={isLoading}
                className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-medium transition-all ${
                  mode === 'autonomous'
                    ? 'bg-gradient-to-r from-indigo-600 to-sky-600 text-white shadow-md shadow-indigo-500/20'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Zap className="w-3.5 h-3.5" />
                <span>Fully Autonomous</span>
              </button>

              <button
                type="button"
                onClick={() => setMode('hitl')}
                disabled={isLoading}
                className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-medium transition-all ${
                  mode === 'hitl'
                    ? 'bg-gradient-to-r from-indigo-600 to-sky-600 text-white shadow-md shadow-indigo-500/20'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <UserCheck className="w-3.5 h-3.5" />
                <span>Human-in-the-Loop</span>
              </button>
            </div>
            <p className="text-[11px] text-slate-400 mt-1.5 px-1">
              {mode === 'autonomous'
                ? '⚡ Continuous execution: Research → Summarize → Write → Critique → Simulated Send.'
                : '⏸ Pauses after Research and Drafting for your review and approval.'}
            </p>
          </div>

          {/* Article Count & Submit */}
          <div className="flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Target Articles ({articleCount})
                </label>
                <span className="text-[11px] text-slate-400">Strictly 5 to 7 articles</span>
              </div>
              <input
                type="range"
                min={5}
                max={7}
                step={1}
                value={articleCount}
                onChange={(e) => setArticleCount(Number(e.target.value))}
                disabled={isLoading}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1 px-1">
                <span>5 Articles</span>
                <span>6 Articles (Recommended)</span>
                <span>7 Articles</span>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading || !goal.trim()}
              className="mt-4 w-full flex items-center justify-center gap-2 bg-gradient-to-r from-sky-500 via-indigo-600 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-white font-semibold py-3 px-6 rounded-xl shadow-lg shadow-indigo-500/25 transition-all transform active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Agent Executing ({activeStatus || 'Processing'})...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-white" />
                  <span>Run Newsletter Agent</span>
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
