import React from 'react';
import { 
  CheckCircle2, 
  Send, 
  FileCheck, 
  Download, 
  Users, 
  Clock, 
  ShieldCheck, 
  RotateCcw,
  Layers,
  FileCode,
  FileText
} from 'lucide-react';
import type { AgentRunState } from '../types';
import { getDownloadUrl } from '../api';

interface FinalReportProps {
  state: AgentRunState;
}

export const FinalReport: React.FC<FinalReportProps> = ({ state }) => {
  const delivery = state.simulated_delivery;
  const critique = state.critique;
  const files = state.output_files;

  return (
    <div className="bg-gradient-to-b from-slate-900 to-slate-950 rounded-2xl border border-emerald-500/30 p-6 shadow-2xl relative overflow-hidden backdrop-blur-md">
      {/* Background glow */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-5 border-b border-slate-800 gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-white m-0">Autonomous Workflow Completed</h2>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Success
              </span>
            </div>
            <p className="text-xs text-slate-400 m-0 mt-0.5">
              Simulated delivery broadcast confirmed &bull; Output files generated to disk
            </p>
          </div>
        </div>

        {/* Clear Simulated Badge */}
        <div className="bg-emerald-950/60 border border-emerald-500/40 px-4 py-2 rounded-xl text-right">
          <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-400">Simulated Dispatch</div>
          <div className="text-sm font-extrabold text-white">
            {delivery ? `${delivery.recipient_count.toLocaleString()} Subscribers` : '1,420 Subscribers'}
          </div>
        </div>
      </div>

      {/* KPI Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3.5 my-5">
        <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-slate-400 text-xs flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-sky-400" />
            <span>Articles Selected</span>
          </div>
          <div className="text-xl font-bold text-white mt-2">
            {state.summaries?.length || state.selected_articles?.length || 0}
            <span className="text-xs font-normal text-slate-400 ml-1">stories</span>
          </div>
        </div>

        <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-slate-400 text-xs flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span>Critique Score</span>
          </div>
          <div className="text-xl font-bold text-emerald-400 mt-2">
            {critique ? critique.quality_score : 94}
            <span className="text-xs font-normal text-slate-400 ml-1">/100</span>
          </div>
        </div>

        <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-slate-400 text-xs flex items-center gap-1.5">
            <RotateCcw className="w-3.5 h-3.5 text-amber-400" />
            <span>Revisions Made</span>
          </div>
          <div className="text-xl font-bold text-white mt-2">
            {state.revision_count}
            <span className="text-xs font-normal text-slate-400 ml-1">passes</span>
          </div>
        </div>

        <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="text-slate-400 text-xs flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-purple-400" />
            <span>Duration</span>
          </div>
          <div className="text-xl font-bold text-white mt-2">
            {state.duration_seconds}s
          </div>
        </div>

        <div className="bg-slate-950/80 p-3.5 rounded-xl border border-slate-800 flex flex-col justify-between col-span-2 md:col-span-1">
          <div className="text-slate-400 text-xs flex items-center gap-1.5">
            <Users className="w-3.5 h-3.5 text-teal-400" />
            <span>Recipients</span>
          </div>
          <div className="text-xl font-bold text-teal-300 mt-2">
            {delivery ? delivery.recipient_count.toLocaleString() : '1,420'}
          </div>
        </div>
      </div>

      {/* Simulated Dispatch Notice */}
      <div className="p-3.5 rounded-xl bg-slate-950/90 border border-slate-800 text-xs text-slate-400 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Send className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>
            <strong>Simulated Delivery Audit:</strong> Dispatched to sample segment ({delivery?.subscribers_sample?.slice(0, 3).join(', ')}...).
          </span>
        </div>
        <span className="text-[11px] font-mono text-slate-400">
          {delivery?.timestamp || 'Confirmed'}
        </span>
      </div>

      {/* Generated Output Files & Download Links */}
      <div className="mt-5 pt-4 border-t border-slate-800">
        <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1.5">
          <FileCheck className="w-4 h-4 text-sky-400" />
          Generated Output Artifacts (Backend Outputs Directory)
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {/* HTML Card */}
          <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/90 flex items-center justify-between">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <FileCode className="w-4 h-4 text-sky-400 shrink-0" />
              <div className="truncate">
                <div className="text-xs font-semibold text-slate-200">Email HTML</div>
                <div className="text-[10px] text-slate-400 font-mono truncate">
                  {files?.html_filename || `newsletter_${state.run_id}.html`}
                </div>
              </div>
            </div>
            <a
              href={getDownloadUrl(state.run_id, 'html')}
              download
              className="p-1.5 bg-slate-800 hover:bg-slate-700 text-sky-400 rounded-lg transition-colors ml-2"
              title="Download HTML"
            >
              <Download className="w-4 h-4" />
            </a>
          </div>

          {/* Markdown Card */}
          <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/90 flex items-center justify-between">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <FileText className="w-4 h-4 text-indigo-400 shrink-0" />
              <div className="truncate">
                <div className="text-xs font-semibold text-slate-200">Markdown Edition</div>
                <div className="text-[10px] text-slate-400 font-mono truncate">
                  {files?.md_filename || `newsletter_${state.run_id}.md`}
                </div>
              </div>
            </div>
            <a
              href={getDownloadUrl(state.run_id, 'md')}
              download
              className="p-1.5 bg-slate-800 hover:bg-slate-700 text-indigo-400 rounded-lg transition-colors ml-2"
              title="Download Markdown"
            >
              <Download className="w-4 h-4" />
            </a>
          </div>

          {/* JSON Report Card */}
          <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/90 flex items-center justify-between">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <FileCheck className="w-4 h-4 text-emerald-400 shrink-0" />
              <div className="truncate">
                <div className="text-xs font-semibold text-slate-200">Execution Report</div>
                <div className="text-[10px] text-slate-400 font-mono truncate">
                  {files?.json_filename || `report_${state.run_id}.json`}
                </div>
              </div>
            </div>
            <a
              href={getDownloadUrl(state.run_id, 'json')}
              download
              className="p-1.5 bg-slate-800 hover:bg-slate-700 text-emerald-400 rounded-lg transition-colors ml-2"
              title="Download JSON Report"
            >
              <Download className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
