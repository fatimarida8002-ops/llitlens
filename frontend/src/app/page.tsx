"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { BookCard } from "@/components/BookCard";
import { ChangeOneThingDrawer } from "@/components/ChangeOneThingDrawer";
import { ComparisonModal } from "@/components/ComparisonModal";
import { ReadingPathView } from "@/components/ReadingPathView";
import { EvaluationDashboard } from "@/components/EvaluationDashboard";
import { SavedHistoryView } from "@/components/SavedHistoryView";

import { discoverBooks, refineRecommendations } from "@/lib/api";
import { Book, ExtractedPreferences } from "@/types";
import { Sparkles, Search, SlidersHorizontal, Scale, ArrowRight, RefreshCw, BookOpen } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"discover" | "history" | "paths" | "evaluation">("discover");
  
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [extractedPrefs, setExtractedPrefs] = useState<ExtractedPreferences | null>(null);
  const [recommendations, setRecommendations] = useState<Book[]>([]);

  // Selection for side-by-side comparison
  const [selectedForCompare, setSelectedForCompare] = useState<string[]>([]);
  const [showComparisonModal, setShowComparisonModal] = useState(false);

  const sampleQueries = [
    "I want a dark mystery under 300 pages with a huge plot twist and almost no romance.",
    "A cozy comforting fantasy with magical world and found family.",
    "Fast-paced sci-fi space exploration without romance.",
    "A book that makes me question everything."
  ];

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await discoverBooks(searchQuery);
      setSessionId(res.session_id);
      setExtractedPrefs(res.extracted_preferences);
      setRecommendations(res.recommendations);
      setSelectedForCompare([]);
    } catch (err: any) {
      setError(err.message || "Failed to process natural language request.");
    } finally {
      setLoading(false);
    }
  };

  const handleRefine = async (instruction: string) => {
    if (!sessionId) return;
    setLoading(true);
    try {
      const res = await refineRecommendations(sessionId, instruction);
      setExtractedPrefs(res.updated_preferences);
      setRecommendations(res.recommendations);
    } catch (err: any) {
      setError(err.message || "Failed to apply refinement.");
    } finally {
      setLoading(false);
    }
  };

  const toggleCompareSelection = (bookId: string) => {
    setSelectedForCompare((prev) =>
      prev.includes(bookId) ? prev.filter((id) => id !== bookId) : [...prev, bookId]
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500 selection:text-white">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "discover" && (
          <div>
            {/* Hero Section */}
            <div className="text-center max-w-3xl mx-auto mb-10">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-4">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                <span>AI-Powered Natural Language Book Discovery</span>
              </div>
              <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight mb-4">
                What do you feel like reading today?
              </h2>
              <p className="text-base text-slate-400 leading-relaxed">
                Describe the experience, mood, atmosphere, or constraints you want in plain natural language.
              </p>
            </div>

            {/* Search Box */}
            <div className="max-w-3xl mx-auto mb-6">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSearch(query);
                }}
                className="relative flex items-center shadow-2xl shadow-indigo-500/10 rounded-2xl overflow-hidden border border-slate-800 bg-slate-900 focus-within:border-indigo-500 transition-all"
              >
                <Search className="w-6 h-6 text-slate-400 absolute left-4 pointer-events-none" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., 'I want a short dark mystery under 300 pages with a huge twist and almost no romance'"
                  className="w-full py-4 pl-14 pr-36 bg-transparent text-base text-white placeholder-slate-500 focus:outline-none"
                />
                <button
                  type="submit"
                  disabled={loading || !query.trim()}
                  className="absolute right-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm flex items-center gap-2 shadow-lg shadow-indigo-500/20 disabled:opacity-50 transition-all"
                >
                  {loading ? (
                    <RefreshCw className="w-4 h-4 animate-spin" />
                  ) : (
                    <Sparkles className="w-4 h-4" />
                  )}
                  <span>Discover</span>
                </button>
              </form>

              {/* Sample Intent Buttons */}
              <div className="mt-3 flex flex-wrap items-center gap-2 justify-center">
                <span className="text-xs font-semibold text-slate-500">Try asking:</span>
                {sampleQueries.map((sq, i) => (
                  <button
                    key={i}
                    onClick={() => {
                      setQuery(sq);
                      handleSearch(sq);
                    }}
                    className="text-xs bg-slate-900/80 border border-slate-800 text-slate-400 hover:text-indigo-300 hover:border-indigo-500/40 px-3 py-1 rounded-full transition-all text-left line-clamp-1 max-w-[280px]"
                  >
                    &quot;{sq}&quot;
                  </button>
                ))}
              </div>
            </div>

            {error && (
              <div className="max-w-3xl mx-auto p-4 rounded-xl bg-rose-950/60 border border-rose-500/40 text-rose-200 text-sm text-center mb-8">
                {error}
              </div>
            )}

            {/* Extracted Reading Intent Banner */}
            {extractedPrefs && (
              <div className="max-w-4xl mx-auto bg-slate-900/90 border border-indigo-500/30 rounded-2xl p-4 mb-8 shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-xl bg-indigo-500/20 text-indigo-400">
                    <SlidersHorizontal className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400">
                      Extracted AI Preferences
                    </span>
                    <h4 className="text-xs text-slate-300 font-medium">
                      System converted your query into structured intent signals
                    </h4>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5">
                  {extractedPrefs.genre && extractedPrefs.genre !== "Any" && (
                    <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-indigo-950 border border-indigo-500/40 text-indigo-300">
                      Genre: {extractedPrefs.genre}
                    </span>
                  )}
                  {extractedPrefs.mood && extractedPrefs.mood !== "Any" && (
                    <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-950 border border-purple-500/40 text-purple-300">
                      Mood: {extractedPrefs.mood}
                    </span>
                  )}
                  {extractedPrefs.max_pages && (
                    <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-cyan-950 border border-cyan-500/40 text-cyan-300">
                      Max Pages: {extractedPrefs.max_pages}
                    </span>
                  )}
                  {extractedPrefs.romance_level && extractedPrefs.romance_level !== "Any" && (
                    <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-pink-950 border border-pink-500/40 text-pink-300">
                      Romance: {extractedPrefs.romance_level}
                    </span>
                  )}
                  {extractedPrefs.pacing && extractedPrefs.pacing !== "Any" && (
                    <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-amber-950 border border-amber-500/40 text-amber-300">
                      Pacing: {extractedPrefs.pacing}
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Conversational Refinement Drawer */}
            {sessionId && (
              <ChangeOneThingDrawer
                onRefine={handleRefine}
                loading={loading}
                activeQuery={query}
              />
            )}

            {/* Recommendations Grid */}
            {recommendations.length > 0 && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                    <BookOpen className="w-5 h-5 text-indigo-400" />
                    Recommended For You
                  </h3>
                  {selectedForCompare.length >= 2 && (
                    <button
                      onClick={() => setShowComparisonModal(true)}
                      className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 animate-pulse"
                    >
                      <Scale className="w-4 h-4" />
                      <span>Compare Selected ({selectedForCompare.length})</span>
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {recommendations.map((book) => (
                    <BookCard
                      key={book.id}
                      book={book}
                      isSelectedForCompare={selectedForCompare.includes(book.id)}
                      onToggleCompare={toggleCompareSelection}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Floating Comparison Drawer */}
            {selectedForCompare.length > 0 && (
              <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 bg-slate-900 border border-indigo-500/50 rounded-2xl px-6 py-3 shadow-2xl flex items-center gap-4 backdrop-blur-md">
                <span className="text-xs font-semibold text-slate-200">
                  {selectedForCompare.length} book(s) selected for side-by-side comparison
                </span>
                <button
                  disabled={selectedForCompare.length < 2}
                  onClick={() => setShowComparisonModal(true)}
                  className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs disabled:opacity-50 transition-all flex items-center gap-1.5"
                >
                  <Scale className="w-4 h-4" />
                  <span>Compare Now</span>
                </button>
              </div>
            )}

            {/* Side-by-Side Comparison Modal */}
            {showComparisonModal && extractedPrefs && (
              <ComparisonModal
                selectedBookIds={selectedForCompare}
                activeIntent={extractedPrefs}
                onClose={() => setShowComparisonModal(false)}
              />
            )}
          </div>
        )}

        {activeTab === "history" && <SavedHistoryView />}
        {activeTab === "paths" && <ReadingPathView />}
        {activeTab === "evaluation" && <EvaluationDashboard />}
      </main>
    </div>
  );
};
