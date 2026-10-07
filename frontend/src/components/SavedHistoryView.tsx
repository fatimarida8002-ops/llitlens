"use client";

import React, { useState, useEffect } from "react";
import { getUserHistory } from "@/lib/api";
import { Bookmark, Check, XCircle, BookOpen, Sparkles } from "lucide-react";

export const SavedHistoryView: React.FC = () => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "saved" | "read" | "rejected">("all");

  useEffect(() => {
    async function fetchHist() {
      setLoading(true);
      try {
        const res = await getUserHistory();
        setHistory(res.history || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchHist();
  }, []);

  const filtered = filter === "all" ? history : history.filter((h) => h.status === filter);

  return (
    <div className="max-w-5xl mx-auto py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <Bookmark className="w-6 h-6 text-purple-400" />
            Personal Reading History & Saved Books
          </h2>
          <p className="text-sm text-slate-400">
            Track saved books, completed reads, and rejected recommendations
          </p>
        </div>

        {/* Status Filter Buttons */}
        <div className="flex gap-1.5 p-1 bg-slate-900 border border-slate-800 rounded-xl">
          {(["all", "saved", "read", "rejected"] as const).map((st) => (
            <button
              key={st}
              onClick={() => setFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all ${
                filter === st
                  ? "bg-purple-600 text-white shadow-md shadow-purple-600/30"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="py-16 text-center text-slate-400 flex flex-col items-center gap-3">
          <Sparkles className="w-8 h-8 text-purple-400 animate-spin" />
          <p className="text-sm font-medium">Loading reading history...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="py-16 text-center text-slate-400 bg-slate-900/40 border border-slate-800/80 rounded-2xl">
          <BookOpen className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <p className="text-base font-semibold text-slate-300">No books found in this status.</p>
          <p className="text-xs text-slate-500">Save or dismiss books from the Discovery tab to populate your history.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 flex gap-4 items-center"
            >
              <div className="w-16 h-24 shrink-0 rounded-lg bg-slate-800 overflow-hidden relative border border-slate-700">
                {item.cover_url ? (
                  <img src={item.cover_url} alt={item.title} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-[10px] font-bold text-slate-400 p-1 text-center">
                    {item.title}
                  </div>
                )}
              </div>

              <div className="flex-1 min-w-0">
                <span
                  className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider mb-1 ${
                    item.status === "saved"
                      ? "bg-indigo-950 text-indigo-300 border border-indigo-500/30"
                      : item.status === "read"
                      ? "bg-emerald-950 text-emerald-300 border border-emerald-500/30"
                      : "bg-rose-950 text-rose-300 border border-rose-500/30"
                  }`}
                >
                  {item.status}
                </span>
                <h4 className="text-base font-bold text-white line-clamp-1">{item.title}</h4>
                <p className="text-xs text-slate-400 font-medium">by {item.author}</p>
                <span className="text-[11px] text-slate-500 block mt-1">📖 {item.pages} pages</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
