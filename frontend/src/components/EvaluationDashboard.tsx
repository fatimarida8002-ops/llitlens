"use client";

import React, { useState, useEffect } from "react";
import { EvaluationExperiment } from "@/types";
import { getEvaluationExperiment } from "@/lib/api";
import { BarChart2, CheckCircle2, AlertTriangle, Sparkles, Filter, Terminal } from "lucide-react";

export const EvaluationDashboard: React.FC = () => {
  const [experiment, setExperiment] = useState<EvaluationExperiment | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function runExp() {
      setLoading(true);
      try {
        const res = await getEvaluationExperiment();
        setExperiment(res);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    runExp();
  }, []);

  return (
    <div className="max-w-5xl mx-auto py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
            <BarChart2 className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Recommendation Quality & Evaluation Dashboard
            </h2>
            <p className="text-sm text-slate-400">
              Precision@K metrics and comparative experiment: Conventional vs Natural Language Search
            </p>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center text-slate-400 flex flex-col items-center gap-3">
          <Sparkles className="w-8 h-8 text-emerald-400 animate-spin" />
          <p className="text-sm font-medium">Running evaluation experiment benchmarks...</p>
        </div>
      ) : experiment ? (
        <div className="space-y-6">
          {/* Test Query Banner */}
          <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex items-center gap-3">
            <Terminal className="w-5 h-5 text-indigo-400 shrink-0" />
            <div className="text-xs">
              <span className="text-slate-400 font-semibold block uppercase tracking-wider mb-0.5">
                Benchmark Test Query
              </span>
              <span className="text-slate-200 font-mono italic">&quot;{experiment.test_query}&quot;</span>
            </div>
          </div>

          {/* Side-by-side Experiment Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Conventional Keyword Search */}
            <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-800 text-slate-300 border border-slate-700">
                    Conventional Keyword Filter
                  </span>
                  <span className="text-xl font-bold text-slate-300">
                    P@5: {experiment.conventional_search.precision_at_5}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-4">
                  Literal keyword search on title/description + hard SQL filter (Genre=Mystery, Pages&lt;320)
                </p>
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-slate-400 block">Top Retrieved Books:</span>
                  <ul className="space-y-1 text-xs text-slate-300">
                    {experiment.conventional_search.top_titles.map((title, i) => (
                      <li key={i} className="flex items-center gap-2 p-2 rounded-lg bg-slate-950/60">
                        <Filter className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                        <span className="line-clamp-1">{title}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Natural Language AI Search */}
            <div className="bg-gradient-to-b from-indigo-950/40 to-slate-900/80 border border-indigo-500/40 rounded-2xl p-6 flex flex-col justify-between shadow-xl shadow-indigo-500/10">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-indigo-600/30 text-indigo-300 border border-indigo-500/50 flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                    LitLens Natural Language AI
                  </span>
                  <span className="text-xl font-bold text-emerald-400">
                    P@5: {experiment.natural_language_search.precision_at_5}
                  </span>
                </div>
                <p className="text-xs text-indigo-200 mb-4">
                  Semantic embeddings + NLU preference extraction + Book DNA hybrid ranking
                </p>
                <div className="space-y-2">
                  <span className="text-xs font-semibold text-indigo-300 block">Top Retrieved Books:</span>
                  <ul className="space-y-1 text-xs text-slate-200">
                    {experiment.natural_language_search.top_titles.map((title, i) => (
                      <li key={i} className="flex items-center justify-between p-2 rounded-lg bg-indigo-950/80 border border-indigo-500/20">
                        <span className="flex items-center gap-2 line-clamp-1">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                          {title}
                        </span>
                        <span className="text-[10px] font-bold text-indigo-300 shrink-0">
                          {Math.round(experiment.natural_language_search.top_scores[i] * 100)}%
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Key Findings Card */}
          <div className="p-5 rounded-2xl bg-emerald-950/30 border border-emerald-500/30 text-xs text-emerald-200 leading-relaxed">
            <h4 className="font-bold text-emerald-300 uppercase tracking-wider mb-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Experiment Key Findings
            </h4>
            <p>{experiment.findings}</p>
          </div>
        </div>
      ) : null}
    </div>
  );
};
