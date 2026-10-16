import React, { useState } from 'react';
import { 
  Eye, 
  Code, 
  FileCode, 
  Copy, 
  Check, 
  Download, 
  Send, 
  RotateCcw, 
  Sparkles,
  MessageSquare
} from 'lucide-react';
import type { AgentRunState } from '../types';
import { getDownloadUrl } from '../api';

interface NewsletterPreviewProps {
  state: AgentRunState | null;
  onApproveNewsletter?: () => void;
  onRequestRevision?: (feedback: string) => void;
  isLoading: boolean;
}

export const NewsletterPreview: React.FC<NewsletterPreviewProps> = ({
  state,
  onApproveNewsletter,
  onRequestRevision,
  isLoading,
}) => {
  const [activeTab, setActiveTab] = useState<'preview' | 'html' | 'markdown'>('preview');
  const [copied, setCopied] = useState<boolean>(false);
  const [showRevisionInput, setShowRevisionInput] = useState<boolean>(false);
  const [revisionFeedback, setRevisionFeedback] = useState<string>('');

  if (!state || (!state.newsletter_html && !state.newsletter_markdown)) {
    return (
      <div className="bg-slate-900/60 rounded-2xl border border-slate-800 p-8 text-center text-slate-500">
        <Eye className="w-8 h-8 mx-auto mb-2 text-slate-600 opacity-60" />
        <p className="text-sm font-medium text-slate-400">Newsletter preview not yet generated</p>
        <p className="text-xs text-slate-500 mt-1">
          Once research and drafting stages complete, the publication preview will appear here.
        </p>
      </div>
    );
  }

  const isHitlWaiting = state.status === 'waiting_newsletter_approval';

  const handleCopy = () => {
    const textToCopy = activeTab === 'markdown' ? state.newsletter_markdown : state.newsletter_html;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRevisionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!revisionFeedback.trim() || !onRequestRevision) return;
    onRequestRevision(revisionFeedback);
    setRevisionFeedback('');
    setShowRevisionInput(false);
  };

  return (
    <div className="bg-slate-900/90 rounded-2xl border border-slate-800 p-6 shadow-xl backdrop-blur-sm">
      {/* Subject Line & Controls Header */}
      <div className="pb-5 border-b border-slate-800 space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Subject Line:</span>
              <span className="text-sm font-bold text-white bg-slate-950/80 px-3 py-1 rounded-lg border border-slate-800">
                {state.subject_line}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Title: <strong className="text-slate-200">{state.newsletter_title}</strong> &bull; Curated {state.summaries?.length || 0} articles
            </p>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>

            <a
              href={getDownloadUrl(state.run_id, 'html')}
              download
              className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-sky-400" />
              <span>HTML</span>
            </a>

            <a
              href={getDownloadUrl(state.run_id, 'md')}
              download
              className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-medium border border-slate-700 transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-indigo-400" />
              <span>Markdown</span>
            </a>
          </div>
        </div>

        {/* HITL Checkpoint Bar */}
        {isHitlWaiting && (
          <div className="bg-gradient-to-r from-amber-500/10 via-indigo-500/10 to-sky-500/10 border border-amber-500/30 p-4 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div className="text-xs font-bold text-amber-300 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                Human Review Checkpoint
              </div>
              <p className="text-xs text-slate-300 mt-0.5 m-0">
                Inspect the drafted newsletter below. You can approve to simulate subscriber delivery or request custom revisions.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowRevisionInput(!showRevisionInput)}
                disabled={isLoading}
                className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-3.5 py-2 rounded-lg font-medium border border-slate-700 transition-all disabled:opacity-50"
              >
                <RotateCcw className="w-3.5 h-3.5 text-amber-400" />
                <span>Request Revision</span>
              </button>

              <button
                onClick={onApproveNewsletter}
                disabled={isLoading}
                className="flex items-center gap-1.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs px-4 py-2 rounded-lg font-bold shadow-lg shadow-emerald-500/20 transition-all disabled:opacity-50"
              >
                <Send className="w-3.5 h-3.5" />
                <span>Approve & Simulate Send</span>
              </button>
            </div>
          </div>
        )}

        {/* Revision Input Form */}
        {showRevisionInput && isHitlWaiting && (
          <form onSubmit={handleRevisionSubmit} className="bg-slate-950 p-4 rounded-xl border border-indigo-500/40 space-y-3">
            <div className="flex items-center gap-2 text-xs font-semibold text-indigo-300">
              <MessageSquare className="w-4 h-4" />
              Editorial Revision Instructions
            </div>
            <textarea
              rows={2}
              value={revisionFeedback}
              onChange={(e) => setRevisionFeedback(e.target.value)}
              placeholder="e.g., Make the editor's note more urgent, focus on enterprise coding benchmarks, or highlight security risks..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 resize-none"
            />
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowRevisionInput(false)}
                className="text-xs text-slate-400 hover:text-slate-200 px-3 py-1"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={!revisionFeedback.trim() || isLoading}
                className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3.5 py-1.5 rounded-lg font-medium shadow transition-all disabled:opacity-50"
              >
                Submit Revision Instructions
              </button>
            </div>
          </form>
        )}

        {/* Tab Switcher */}
        <div className="flex items-center gap-2 pt-1">
          <button
            onClick={() => setActiveTab('preview')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'preview'
                ? 'bg-indigo-600 text-white shadow'
                : 'bg-slate-950/70 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Responsive Email Preview</span>
          </button>

          <button
            onClick={() => setActiveTab('markdown')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'markdown'
                ? 'bg-indigo-600 text-white shadow'
                : 'bg-slate-950/70 text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileCode className="w-3.5 h-3.5" />
            <span>Markdown View</span>
          </button>

          <button
            onClick={() => setActiveTab('html')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'html'
                ? 'bg-indigo-600 text-white shadow'
                : 'bg-slate-950/70 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Code className="w-3.5 h-3.5" />
            <span>Raw HTML Source</span>
          </button>
        </div>
      </div>

      {/* Content Rendering Container */}
      <div className="mt-5">
        {activeTab === 'preview' && (
          <div className="rounded-xl overflow-hidden border border-slate-800 bg-slate-950 shadow-inner">
            <iframe
              srcDoc={state.newsletter_html}
              title="Newsletter Preview"
              className="w-full h-[640px] border-none bg-slate-950"
              sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin"
            />
          </div>
        )}

        {activeTab === 'markdown' && (
          <div className="rounded-xl overflow-hidden border border-slate-800 bg-slate-950 p-5 shadow-inner">
            <pre className="text-xs font-mono text-slate-300 whitespace-pre-wrap overflow-x-auto max-h-[640px] leading-relaxed">
              {state.newsletter_markdown}
            </pre>
          </div>
        )}

        {activeTab === 'html' && (
          <div className="rounded-xl overflow-hidden border border-slate-800 bg-slate-950 p-5 shadow-inner">
            <pre className="text-xs font-mono text-sky-300 whitespace-pre-wrap overflow-x-auto max-h-[640px] leading-relaxed">
              {state.newsletter_html}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};
