"use client";

import React, { useState, useEffect } from "react";
import { ComparisonData, ExtractedPreferences } from "@/types";
import { compareBooks } from "@/lib/api";
import { X, Trophy, CheckCircle, Scale, Sparkles } from "lucide-react";

interface ComparisonModalProps {
  selectedBookIds: string[];
  activeIntent: ExtractedPreferences;
  onClose: () => void;
}

export const ComparisonModal: React.FC<ComparisonModalProps> = ({
  selectedBookIds,
  activeIntent,
  onClose,
}) => {
  const [data, setData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchComparison() {
      try {
        setLoading(true);
        const result = await compareBooks(selectedBookIds, activeIntent);
        setData(result);
      } catch (err: any) {
        setError(err.message || "Failed to compare books.");
      } finally {
        setLoading(false);
      }
    }
    if (selectedBookIds.length >= 2) {
      fetchComparison();
    }
  }, [selectedBookIds, activeIntent]);

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl max-w-4xl w-full p-6 shadow-2xl relative max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
            <Scale className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">
              Preference-Aware Side-by-Side Comparison
            </h2>
            <p className="text-xs text-slate-400">
              Evaluates candidate books directly against your active intent
            </p>
          </div>
        </div>

        {loading ? (
          <div className="py-12 text-center text-slate-400 flex flex-col items-center gap-3">
            <Sparkles className="w-8 h-8 text-indigo-400 animate-spin" />
            <p className="text-sm font-medium">Analyzing books against your intent...</p>
          </div>
        ) : error ? (
          <div className="py-8 text-center text-rose-400 text-sm">{error}</div>
        ) : data ? (
          <div>
            {/* Verdict Banner */}
            <div className="p-4 rounded-2xl bg-gradient-to-r from-indigo-950/80 via-purple-950/80 to-slate-900 border border-indigo-500/30 mb-6 flex items-start gap-3">
              <Trophy className="w-6 h-6 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold text-indigo-300 uppercase tracking-wider mb-1">
                  AI Recommendation Verdict
                </h4>
                <p className="text-sm text-white font-medium">{data.verdict}</p>
              </div>
            </div>

            {/* Comparison Matrix Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-800">
                    <th className="p-3 text-xs font-semibold text-slate-400 uppercase">Attribute</th>
                    {data.compared_books.map((b) => (
                      <th key={b.id} className="p-3 text-sm font-bold text-white min-w-[200px]">
                        {b.title}
                        <span className="block text-xs font-normal text-slate-400">by {b.author}</span>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-xs">
                  <tr>
                    <td className="p-3 font-semibold text-slate-400">Length</td>
                    {data.compared_books.map((b) => (
                      <td key={b.id} className="p-3 text-slate-200">
                        {b.pages} pages
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-400">Mood</td>
                    {data.compared_books.map((b) => (
                      <td key={b.id} className="p-3 text-slate-200 font-medium">
                        {b.book_dna?.mood || "Balanced"}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-400">Pacing</td>
                    {data.compared_books.map((b) => (
                      <td key={b.id} className="p-3 text-slate-200">
                        {b.book_dna?.pacing || "Medium"}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-400">Romance Level</td>
                    {data.compared_books.map((b) => (
                      <td key={b.id} className="p-3 text-slate-200">
                        {b.book_dna?.romance_level || "Medium"}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-400">Complexity</td>
                    {data.compared_books.map((b) => (
                      <td key={b.id} className="p-3 text-slate-200">
                        {b.book_dna?.complexity || "Medium"}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-semibold text-slate-400">Intent Strengths</td>
                    {data.compared_books.map((b) => {
                      const item = data.analysis.find((a) => a.book_id === b.id);
                      return (
                        <td key={b.id} className="p-3">
                          <ul className="space-y-1">
                            {item?.strengths.map((str, idx) => (
                              <li key={idx} className="flex items-center gap-1.5 text-emerald-300">
                                <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                                <span>{str}</span>
                              </li>
                            ))}
                          </ul>
                        </td>
                      );
                    })}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};
