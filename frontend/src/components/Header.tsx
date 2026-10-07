"use client";

import React from "react";
import { BookOpen, Sparkles, Layers, BarChart2, Bookmark } from "lucide-react";

interface HeaderProps {
  activeTab: "discover" | "history" | "paths" | "evaluation";
  setActiveTab: (tab: "discover" | "history" | "paths" | "evaluation") => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab }) => {
  return (
    <header className="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab("discover")}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 p-[2px] shadow-lg shadow-indigo-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-indigo-400" />
            </div>
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-200 via-white to-purple-200 bg-clip-text text-transparent tracking-tight">
              LitLens
            </h1>
            <p className="text-[10px] text-slate-400 font-medium uppercase tracking-widest">
              AI Natural Language Discovery
            </p>
          </div>
        </div>

        <nav className="flex items-center gap-1 sm:gap-2">
          <button
            onClick={() => setActiveTab("discover")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "discover"
                ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
            }`}
          >
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span>Discover</span>
          </button>

          <button
            onClick={() => setActiveTab("history")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "history"
                ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
            }`}
          >
            <Bookmark className="w-4 h-4 text-purple-400" />
            <span>Saved & History</span>
          </button>

          <button
            onClick={() => setActiveTab("paths")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "paths"
                ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
            }`}
          >
            <Layers className="w-4 h-4 text-pink-400" />
            <span>Reading Paths</span>
          </button>

          <button
            onClick={() => setActiveTab("evaluation")}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
              activeTab === "evaluation"
                ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
            }`}
          >
            <BarChart2 className="w-4 h-4 text-emerald-400" />
            <span>Evaluation</span>
          </button>
        </nav>
      </div>
    </header>
  );
};
