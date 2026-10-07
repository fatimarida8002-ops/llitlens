"use client";

import React from "react";
import { BookDNA } from "@/types";

interface BookDnaPillsProps {
  dna: BookDNA;
  compact?: boolean;
}

export const BookDnaPills: React.FC<BookDnaPillsProps> = ({ dna, compact = false }) => {
  if (!dna) return null;

  const moodColors: Record<string, string> = {
    Dark: "bg-slate-900 border-purple-500/40 text-purple-300",
    Suspenseful: "bg-amber-950/60 border-amber-500/40 text-amber-300",
    Comforting: "bg-emerald-950/60 border-emerald-500/40 text-emerald-300",
    "Thought-provoking": "bg-cyan-950/60 border-cyan-500/40 text-cyan-300",
    Atmospheric: "bg-indigo-950/60 border-indigo-500/40 text-indigo-300",
    Uplifting: "bg-rose-950/60 border-rose-500/40 text-rose-300",
    Funny: "bg-yellow-950/60 border-yellow-500/40 text-yellow-300",
    Mysterious: "bg-violet-950/60 border-violet-500/40 text-violet-300",
  };

  const currentMoodClass = moodColors[dna.mood] || "bg-slate-800 border-slate-700 text-slate-300";

  return (
    <div className="flex flex-wrap gap-1.5 items-center">
      <span className={`px-2 py-0.5 text-xs font-semibold rounded-md border ${currentMoodClass}`}>
        Mood: {dna.mood}
      </span>
      <span className="px-2 py-0.5 text-xs font-medium rounded-md border border-slate-800 bg-slate-900/80 text-slate-300">
        Pacing: {dna.pacing}
      </span>
      <span className="px-2 py-0.5 text-xs font-medium rounded-md border border-slate-800 bg-slate-900/80 text-slate-300">
        Romance: {dna.romance_level}
      </span>
      <span className="px-2 py-0.5 text-xs font-medium rounded-md border border-slate-800 bg-slate-900/80 text-slate-300">
        Complexity: {dna.complexity}
      </span>
      {!compact && dna.setting && (
        <span className="px-2 py-0.5 text-xs font-medium rounded-md border border-slate-800 bg-slate-900/60 text-slate-400">
          📍 {dna.setting}
        </span>
      )}
    </div>
  );
};
