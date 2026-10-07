"use client";

import React, { useState } from "react";
import { Sparkles, SlidersHorizontal, ArrowRight, RefreshCw } from "lucide-react";

interface ChangeOneThingDrawerProps {
  onRefine: (instruction: string) => void;
  loading: boolean;
  activeQuery?: string;
}

export const ChangeOneThingDrawer: React.FC<ChangeOneThingDrawerProps> = ({
  onRefine,
  loading,
  activeQuery,
}) => {
  const [customRefinement, setCustomRefinement] = useState("");

  const presetRefinements = [
    { label: "🌙 Make it darker", value: "Make it darker" },
    { label: "📖 Shorter (< 300 pages)", value: "Shorter under 300 pages" },
    { label: "💖 Less romance", value: "Less romance" },
    { label: "⚡ Faster pacing", value: "Faster pacing" },
    { label: "🧘 Easier to read", value: "Easier to read" },
    { label: "💡 More thought-provoking", value: "More thought-provoking" },
  ];

  const handleSubmitCustom = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customRefinement.trim()) return;
    onRefine(customRefinement);
    setCustomRefinement("");
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 mb-8 shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base font-bold text-white tracking-tight">
            Conversational Refinement (&quot;Change One Thing&quot;)
          </h3>
        </div>
        <span className="text-xs text-slate-400 font-medium">
          Preserves your query context while adjusting preferences
        </span>
      </div>

      {/* Preset Refinement Pills */}
      <div className="flex flex-wrap gap-2 mb-4">
        {presetRefinements.map((preset) => (
          <button
            key={preset.value}
            disabled={loading}
            onClick={() => onRefine(preset.value)}
            className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800/90 text-slate-200 border border-slate-700/80 hover:bg-indigo-600 hover:text-white hover:border-indigo-500 transition-all shadow-sm"
          >
            {preset.label}
          </button>
        ))}
      </div>

      {/* Custom Conversational Input */}
      <form onSubmit={handleSubmitCustom} className="flex gap-2">
        <input
          type="text"
          value={customRefinement}
          onChange={(e) => setCustomRefinement(e.target.value)}
          placeholder='Or type a refinement: e.g. "Keep everything but make it set in space"'
          className="flex-1 px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
        />
        <button
          type="submit"
          disabled={loading || !customRefinement.trim()}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm flex items-center gap-2 disabled:opacity-50 transition-all shadow-md shadow-indigo-600/20"
        >
          {loading ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <Sparkles className="w-4 h-4" />
          )}
          <span>Refine</span>
        </button>
      </form>
    </div>
  );
};
