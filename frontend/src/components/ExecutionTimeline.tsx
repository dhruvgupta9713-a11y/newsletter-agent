import React from 'react';
import { 
  Compass, 
  Search, 
  FileText, 
  PenTool, 
  ShieldCheck, 
  RotateCcw, 
  Send, 
  CheckCircle2,
  Clock,
  Loader2
} from 'lucide-react';
import type { AgentRunState } from '../types';

interface ExecutionTimelineProps {
  state: AgentRunState | null;
  isLoading: boolean;
}

interface StepConfig {
  key: string;
  name: string;
  desc: string;
  icon: React.ComponentType<{ className?: string }>;
}

const TIMELINE_STEPS: StepConfig[] = [
  { key: 'planning', name: 'Planning', desc: 'Goal analysis & search strategy', icon: Compass },
  { key: 'researching', name: 'Researching', desc: 'Querying news & URL validation', icon: Search },
  { key: 'summarizing', name: 'Summarizing', desc: 'Selecting 5-7 articles & key takeaways', icon: FileText },
  { key: 'writing', name: 'Writing', desc: 'Drafting responsive HTML & Markdown', icon: PenTool },
  { key: 'critiquing', name: 'Self-Review', desc: 'Deterministic check & quality score', icon: ShieldCheck },
  { key: 'revising', name: 'Revising', desc: 'Automated editorial refinements', icon: RotateCcw },
  { key: 'sending', name: 'Sending Simulation', desc: 'Simulated dispatch & file export', icon: Send },
  { key: 'completed', name: 'Completed', desc: 'Publication artifact ready', icon: CheckCircle2 },
];

export const ExecutionTimeline: React.FC<ExecutionTimelineProps> = ({ state, isLoading }) => {
  if (!state) {
    return (
      <div className="bg-slate-900/60 rounded-2xl border border-slate-800/80 p-5 text-center text-slate-500 text-sm">
        Start an execution to observe the live LangGraph agent lifecycle.
      </div>
    );
  }

  const currentStatus = state.status;
  const isCompleted = currentStatus === 'completed';

  // Map state status to step order index
  const getStepIndex = (status: string): number => {
    switch (status) {
      case 'planning': return 0;
      case 'researching':
      case 'waiting_research_approval': return 1;
      case 'summarizing': return 2;
      case 'writing': return 3;
      case 'critiquing':
      case 'self_review': return 4;
      case 'revising': return 5;
      case 'sending':
      case 'waiting_newsletter_approval': return 6;
      case 'completed': return 7;
      default: return 0;
    }
  };

  const currentIndex = getStepIndex(currentStatus);

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-800 gap-2">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2 m-0">
            <Clock className="w-4 h-4 text-sky-400" />
            Execution Timeline & LangGraph State
          </h2>
          <p className="text-xs text-slate-400 m-0 mt-0.5">
            Run ID: <span className="font-mono text-slate-300">{state.run_id}</span> &bull; Mode: <span className="capitalize text-indigo-400 font-medium">{state.mode}</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          {state.duration_seconds > 0 && (
            <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-full border border-slate-700">
              Duration: <strong>{state.duration_seconds}s</strong>
            </span>
          )}
          <span className={`text-xs px-3 py-1 rounded-full font-medium uppercase tracking-wider ${
            isCompleted 
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
              : currentStatus.startsWith('waiting')
              ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30 animate-pulse'
              : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30'
          }`}>
            {currentStatus.replace(/_/g, ' ')}
          </span>
        </div>
      </div>

      {/* Progress Step Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3 pt-5">
        {TIMELINE_STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isPassed = isCompleted || idx < currentIndex;
          const isCurrent = idx === currentIndex && !isCompleted;
          const isWaiting = isCurrent && currentStatus.startsWith('waiting');

          return (
            <div 
              key={step.key}
              className={`flex flex-col items-center text-center p-3 rounded-xl border transition-all ${
                isWaiting
                  ? 'bg-amber-500/10 border-amber-500/40 shadow-lg shadow-amber-500/10'
                  : isCurrent
                  ? 'bg-indigo-500/10 border-indigo-500/40 shadow-lg shadow-indigo-500/10'
                  : isPassed
                  ? 'bg-slate-950/60 border-slate-800 text-slate-300'
                  : 'bg-slate-950/30 border-slate-900 opacity-40 text-slate-600'
              }`}
            >
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center mb-2.5 transition-all ${
                isWaiting
                  ? 'bg-amber-500 text-slate-950 font-bold'
                  : isCurrent
                  ? 'bg-indigo-600 text-white animate-pulse'
                  : isPassed
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                  : 'bg-slate-800 text-slate-500'
              }`}>
                {isWaiting ? (
                  <span className="text-xs font-bold">HITL</span>
                ) : isCurrent && isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : isPassed ? (
                  <CheckCircle2 className="w-4 h-4" />
                ) : (
                  <Icon className="w-4 h-4" />
                )}
              </div>

              <span className={`text-xs font-semibold leading-tight ${
                isWaiting ? 'text-amber-300' : isCurrent ? 'text-indigo-300' : isPassed ? 'text-slate-200' : 'text-slate-500'
              }`}>
                {step.name}
              </span>
              <span className="text-[10px] text-slate-500 mt-1 line-clamp-2 leading-tight">
                {step.desc}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
