import React, { useState } from 'react';
import { Terminal, CheckCircle2, AlertTriangle, AlertCircle, ChevronDown, ChevronUp, Wrench, ShieldAlert } from 'lucide-react';
import type { ActivityLogEntry, CritiqueData } from '../types';

interface AgentActivityLogProps {
  logs: ActivityLogEntry[];
  critique?: CritiqueData | null;
  revisionCount?: number;
}

export const AgentActivityLog: React.FC<AgentActivityLogProps> = ({ logs, critique, revisionCount = 0 }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (!logs || logs.length === 0) {
    return (
      <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-6 text-center text-slate-500 text-sm">
        <Terminal className="w-6 h-6 mx-auto mb-2 text-slate-600 opacity-60" />
        No agent actions recorded yet.
      </div>
    );
  }

  const toggleExpand = (idx: number) => {
    setExpandedIndex(expandedIndex === idx ? null : idx);
  };

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2 m-0">
            <Terminal className="w-4 h-4 text-emerald-400" />
            Agent Activity & Self-Reflection Log
          </h2>
          <p className="text-xs text-slate-400 m-0 mt-0.5">
            Transparent chronological record of tool invocations, editorial decisions, and verification checks.
          </p>
        </div>

        {/* Critique score pill if available */}
        {critique && (
          <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-700">
            <span className="text-xs text-slate-400">Quality Score:</span>
            <span className={`text-sm font-bold ${
              critique.quality_score >= 85 ? 'text-emerald-400' : 'text-amber-400'
            }`}>
              {critique.quality_score}/100
            </span>
            {revisionCount > 0 && (
              <span className="text-[10px] bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded border border-indigo-500/30">
                {revisionCount} {revisionCount === 1 ? 'Revision' : 'Revisions'}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Critique Self-Reflection Card if issues or suggestions exist */}
      {critique && (critique.issues?.length > 0 || critique.suggestions?.length > 0) && (
        <div className="my-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
              <ShieldAlert className="w-3.5 h-3.5 text-sky-400" />
              Editorial Review Findings
            </span>
            <span className="text-[11px] text-slate-400">
              Deterministic checks: {critique.deterministic_checks?.article_count_valid ? 'Passed' : 'Failed'} &bull; URLs verified: {critique.deterministic_checks?.urls_verified_count}
            </span>
          </div>

          {critique.issues?.length > 0 && (
            <div className="space-y-1">
              <span className="text-[11px] font-semibold text-amber-400">Identified Issues:</span>
              <ul className="text-xs text-slate-300 pl-4 list-disc space-y-0.5">
                {critique.issues.map((issue, idx) => (
                  <li key={idx}>{issue}</li>
                ))}
              </ul>
            </div>
          )}

          {critique.suggestions?.length > 0 && (
            <div className="space-y-1">
              <span className="text-[11px] font-semibold text-sky-400">Improvement Suggestions:</span>
              <ul className="text-xs text-slate-300 pl-4 list-disc space-y-0.5">
                {critique.suggestions.map((sug, idx) => (
                  <li key={idx}>{sug}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Log Entries Stream */}
      <div className="space-y-2.5 mt-4">
        {logs.map((log, idx) => {
          const isExpanded = expandedIndex === idx;
          const hasDetails = log.details && Object.keys(log.details).length > 0;

          return (
            <div
              key={idx}
              className="bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 rounded-xl p-3.5 transition-all text-xs"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-2.5">
                  <div className="mt-0.5">
                    {log.status === 'success' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : log.status === 'warning' ? (
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-rose-400" />
                    )}
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-slate-200">{log.step}</span>
                      <span className="font-mono text-[10px] bg-slate-800 text-sky-300 px-2 py-0.5 rounded border border-slate-700/60 flex items-center gap-1">
                        <Wrench className="w-2.5 h-2.5" />
                        {log.tool_name}
                      </span>
                      <span className="text-[11px] text-slate-400">{log.timestamp}</span>
                    </div>

                    <p className="text-slate-300 mt-1 m-0 leading-relaxed font-sans">
                      {log.description}
                    </p>
                  </div>
                </div>

                {hasDetails && (
                  <button
                    onClick={() => toggleExpand(idx)}
                    className="text-slate-400 hover:text-slate-200 p-1 rounded hover:bg-slate-800 transition-colors"
                    title="Toggle details"
                  >
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                )}
              </div>

              {/* Collapsible raw details */}
              {isExpanded && hasDetails && (
                <div className="mt-3 pt-3 border-t border-slate-800/80">
                  <pre className="text-[11px] font-mono text-slate-400 bg-slate-900 p-2.5 rounded-lg overflow-x-auto max-h-48 border border-slate-800">
                    {JSON.stringify(log.details, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
