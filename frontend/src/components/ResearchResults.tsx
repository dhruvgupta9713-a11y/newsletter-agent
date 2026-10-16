import React, { useState } from 'react';
import { ExternalLink, Check, Search, Filter, ArrowRight } from 'lucide-react';
import type { Article, AgentRunState } from '../types';

interface ResearchResultsProps {
  state: AgentRunState | null;
  onApproveResearch?: (approvedArticles: Article[]) => void;
  isLoading: boolean;
}

export const ResearchResults: React.FC<ResearchResultsProps> = ({ state, onApproveResearch, isLoading }) => {
  if (!state || (!state.raw_articles?.length && !state.selected_articles?.length)) {
    return (
      <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-8 text-center text-slate-500">
        <Search className="w-8 h-8 mx-auto mb-2 text-slate-600 opacity-60" />
        <p className="text-sm font-medium text-slate-400">No research articles loaded yet</p>
        <p className="text-xs text-slate-500 mt-1">Submit an objective to initiate automated AI search and deduplication.</p>
      </div>
    );
  }

  const isHitlWaiting = state.status === 'waiting_research_approval';
  const initialArticles = state.selected_articles?.length ? state.selected_articles : state.raw_articles;
  
  // Local state for article selection in HITL mode
  const [selectedMap, setSelectedMap] = useState<Record<string, boolean>>(() => {
    const map: Record<string, boolean> = {};
    initialArticles.forEach((a) => {
      map[a.url] = a.approved !== false;
    });
    return map;
  });

  const toggleSelect = (url: string) => {
    if (!isHitlWaiting) return;
    setSelectedMap(prev => ({
      ...prev,
      [url]: !prev[url]
    }));
  };

  const handleApprove = () => {
    if (!onApproveResearch) return;
    const approvedList = initialArticles.filter(a => selectedMap[a.url] !== false);
    onApproveResearch(approvedList);
  };

  const selectedCount = Object.values(selectedMap).filter(Boolean).length;

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl backdrop-blur-sm">
      {/* Header and Query Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-base font-bold text-white flex items-center gap-2 m-0">
            <Filter className="w-4 h-4 text-sky-400" />
            Research Intelligence ({initialArticles.length} Verified Articles)
          </h2>
          <p className="text-xs text-slate-400 m-0 mt-0.5">
            Deduplicated canonical sources targeting AI agents, multi-agent frameworks, and coding workflows.
          </p>
        </div>

        {/* HITL Action Controls */}
        {isHitlWaiting && (
          <div className="flex items-center gap-3 bg-amber-500/10 border border-amber-500/30 px-4 py-2 rounded-xl">
            <div className="text-xs">
              <span className="font-semibold text-amber-300">Human Checkpoint:</span>{' '}
              <span className="text-slate-300">{selectedCount} articles approved</span>
            </div>
            <button
              onClick={handleApprove}
              disabled={isLoading || selectedCount < 5}
              className="flex items-center gap-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-3 py-1.5 rounded-lg text-xs shadow transition-all disabled:opacity-50"
            >
              <span>Approve & Continue</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>

      {/* Search Queries Used */}
      {state.search_queries?.length > 0 && (
        <div className="py-3 px-3.5 my-4 bg-slate-950/70 rounded-xl border border-slate-800/80 flex flex-wrap items-center gap-2">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Search className="w-3 h-3 text-indigo-400" /> Queries:
          </span>
          {state.search_queries.map((q, idx) => (
            <span key={idx} className="text-xs bg-slate-800/90 text-slate-300 px-2.5 py-0.5 rounded-md border border-slate-700/60 font-mono">
              "{q}"
            </span>
          ))}
        </div>
      )}

      {/* Articles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
        {initialArticles.map((article, idx) => {
          const isSelected = selectedMap[article.url] !== false;
          return (
            <div
              key={idx}
              onClick={() => toggleSelect(article.url)}
              className={`p-4 rounded-xl border transition-all flex flex-col justify-between ${
                isHitlWaiting ? 'cursor-pointer' : ''
              } ${
                isSelected
                  ? 'bg-slate-950/80 border-slate-700/80 hover:border-indigo-500/50'
                  : 'bg-slate-950/30 border-slate-900 opacity-50'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20">
                      {article.source}
                    </span>
                    <span className="text-[11px] text-slate-400">
                      {article.published_date || 'Recent'}
                    </span>
                  </div>

                  {/* Selection Checkbox */}
                  {isHitlWaiting && (
                    <div className={`w-5 h-5 rounded flex items-center justify-center border transition-all ${
                      isSelected ? 'bg-indigo-600 border-indigo-500 text-white' : 'border-slate-600 bg-slate-800'
                    }`}>
                      {isSelected && <Check className="w-3.5 h-3.5" />}
                    </div>
                  )}
                </div>

                <h3 className="text-sm font-semibold text-slate-100 hover:text-sky-300 transition-colors line-clamp-2 m-0">
                  {article.title}
                </h3>

                <p className="text-xs text-slate-400 mt-2 line-clamp-3 leading-relaxed">
                  {article.snippet}
                </p>
              </div>

              <div className="pt-3 mt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-[11px] text-slate-400 font-mono">
                  {new URL(article.url).hostname}
                </span>

                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="inline-flex items-center gap-1 text-sky-400 hover:text-sky-300 hover:underline text-xs"
                >
                  <span>Source</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
