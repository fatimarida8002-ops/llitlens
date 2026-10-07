"use client";

import React, { useState, useEffect } from "react";
import { ReadingPath } from "@/types";
import { getReadingPath } from "@/lib/api";
import { Layers, ArrowRight, BookOpen, CheckCircle, Sparkles } from "lucide-react";

export const ReadingPathView: React.FC = () => {
  const [topic, setTopic] = useState("Fantasy");
  const [pathData, setPathData] = useState<ReadingPath | null>(null);
  const [loading, setLoading] = useState(false);

  const genres = ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Literary"];

  useEffect(() => {
    async function fetchPath() {
      setLoading(true);
      try {
        const res = await getReadingPath(topic);
        setPathData(res);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchPath();
  }, [topic]);

  return (
    <div className="max-w-5xl mx-auto py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-3 rounded-2xl bg-pink-500/10 border border-pink-500/20 text-pink-400">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Progressive AI Reading Paths
            </h2>
            <p className="text-sm text-slate-400">
              Guided journey ordering books by complexity, length, and narrative depth
            </p>
          </div>
        </div>

        {/* Genre Selector Pills */}
        <div className="flex flex-wrap gap-2 mt-4">
          {genres.map((g) => (
            <button
              key={g}
              onClick={() => setTopic(g)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                topic === g
                  ? "bg-pink-600 text-white shadow-lg shadow-pink-600/30"
                  : "bg-slate-900 border border-slate-800 text-slate-300 hover:border-slate-700"
              }`}
            >
              {g} Path
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center text-slate-400 flex flex-col items-center gap-3">
          <Sparkles className="w-8 h-8 text-pink-400 animate-spin" />
          <p className="text-sm font-medium">Generating progressive reading sequence...</p>
        </div>
      ) : pathData ? (
        <div className="space-y-6">
          {pathData.steps.map((step, idx) => (
            <div
              key={step.step}
              className="relative bg-slate-900/60 border border-slate-800/80 rounded-2xl p-6 hover:border-pink-500/30 transition-all flex flex-col md:flex-row gap-6 items-start md:items-center justify-between shadow-xl"
            >
              {/* Step Number Badge */}
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center text-white font-black text-lg shadow-lg shadow-pink-500/20 shrink-0">
                  0{step.step}
                </div>

                <div>
                  <span className="text-xs font-bold text-pink-400 uppercase tracking-wider block mb-1">
                    {step.stage}
                  </span>
                  <h3 className="text-xl font-bold text-white tracking-tight">{step.title}</h3>
                  <p className="text-sm font-medium text-slate-400">by {step.author}</p>
                </div>
              </div>

              {/* Attributes & Progression Reason */}
              <div className="flex-1 md:max-w-md">
                <div className="flex items-center gap-3 text-xs text-slate-400 mb-2">
                  <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 font-semibold text-slate-200">
                    Complexity: {step.complexity}
                  </span>
                  <span>📖 {step.pages} pages</span>
                </div>
                <p className="text-xs text-slate-300 bg-slate-950/70 p-3 rounded-xl border border-slate-800/80 leading-relaxed">
                  {step.reason}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
};
