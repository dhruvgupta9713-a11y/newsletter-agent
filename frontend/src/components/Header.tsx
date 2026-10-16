import React from 'react';
import { Bot, Sparkles, Search, CheckCircle2, AlertTriangle } from 'lucide-react';
import type { SystemStatus } from '../types';

interface HeaderProps {
  status: SystemStatus | null;
  loading?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ status }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-sky-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white m-0">Newsletter Agent</h1>
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                Autonomous
              </span>
            </div>
            <p className="text-xs text-slate-400 m-0">Autonomous AI-powered newsletter research, synthesis & simulated delivery</p>
          </div>
        </div>

        {/* Integration Status Badges */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* LLM Status */}
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            <span className="text-slate-400">LLM:</span>
            <span className="font-medium text-slate-200">
              {status?.openai_configured ? status.openai_model : 'Simulation Engine'}
            </span>
            {status?.openai_configured ? (
              <CheckCircle2 className="w-3 h-3 text-emerald-400 ml-0.5" />
            ) : (
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400 ml-0.5" title="Operating in simulated fallback" />
            )}
          </div>

          {/* Search Status */}
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs">
            <Search className="w-3.5 h-3.5 text-indigo-400" />
            <span className="text-slate-400">Search:</span>
            <span className="font-medium text-slate-200">
              {status?.tavily_configured ? 'Tavily Search API' : 'Curated Intelligence'}
            </span>
            {status?.tavily_configured ? (
              <CheckCircle2 className="w-3 h-3 text-emerald-400 ml-0.5" />
            ) : (
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400 ml-0.5" title="Curated verified sample data" />
            )}
          </div>

          {/* Demo Mode Badge */}
          {status?.demo_mode && (
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-medium">
              <AlertTriangle className="w-3.5 h-3.5" />
              <span>Demo Mode Active</span>
            </div>
          )}

          {/* System Health */}
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Ready</span>
          </div>
        </div>
      </div>
    </header>
  );
};
