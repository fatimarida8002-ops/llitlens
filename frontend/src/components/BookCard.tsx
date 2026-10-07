"use client";

import React, { useState } from "react";
import { Book } from "@/types";
import { BookDnaPills } from "./BookDnaPills";
import { BookAvailability } from "./BookAvailability";
import { Bookmark, Check, ShieldAlert, Sparkles, CheckSquare, Square, XCircle } from "lucide-react";
import { updateBookStatus } from "@/lib/api";

interface BookCardProps {
  book: Book;
  isSelectedForCompare: boolean;
  onToggleCompare: (bookId: string) => void;
  onStatusChanged?: () => void;
}

export const BookCard: React.FC<BookCardProps> = ({
  book,
  isSelectedForCompare,
  onToggleCompare,
  onStatusChanged,
}) => {
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleStatusUpdate = async (newStatus: string) => {
    setLoading(true);
    try {
      await updateBookStatus(book.id, newStatus);
      setStatus(newStatus);
      if (onStatusChanged) onStatusChanged();
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const matchPercent = book.match_score ? Math.round(book.match_score * 100) : 85;

  return (
    <div
      className={`group relative bg-slate-900/60 border rounded-2xl p-5 transition-all duration-300 flex flex-col justify-between hover:shadow-2xl hover:shadow-indigo-500/10 ${
        isSelectedForCompare
          ? "border-indigo-500 ring-2 ring-indigo-500/30 bg-slate-900/90"
          : "border-slate-800/80 hover:border-slate-700"
      }`}
    >
      <div>
        {/* Top Header: Match Badge & Compare Button */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-indigo-500/20 to-purple-500/20 text-indigo-300 border border-indigo-500/30">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
              {matchPercent}% Compatibility
            </span>
          </div>

          <button
            onClick={() => onToggleCompare(book.id)}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
              isSelectedForCompare
                ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                : "bg-slate-800/80 text-slate-300 hover:bg-slate-800"
            }`}
          >
            {isSelectedForCompare ? (
              <CheckSquare className="w-3.5 h-3.5 text-white" />
            ) : (
              <Square className="w-3.5 h-3.5 text-slate-400" />
            )}
            <span>{isSelectedForCompare ? "Comparing" : "Compare"}</span>
          </button>
        </div>

        {/* Content Layout */}
        <div className="flex gap-4">
          {/* Book Cover Placeholder / Image */}
          <div className="w-24 h-36 shrink-0 rounded-xl bg-gradient-to-br from-slate-800 via-indigo-950 to-slate-900 border border-slate-700/60 shadow-md overflow-hidden relative group-hover:scale-[1.02] transition-transform">
            {book.cover_url ? (
              <img
                src={book.cover_url}
                alt={book.title}
                className="w-full h-full object-cover"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = "none";
                }}
              />
            ) : null}
            <div className="w-full h-full p-2 flex flex-col justify-between bg-slate-900/90 text-center">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 line-clamp-2">
                {book.title}
              </span>
              <span className="text-[9px] text-slate-400 line-clamp-1">{book.author}</span>
            </div>
          </div>

          {/* Title, Author & Description */}
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-bold text-white tracking-tight group-hover:text-indigo-300 transition-colors line-clamp-1">
              {book.title}
            </h3>
            <p className="text-sm font-medium text-slate-400 mb-2">by {book.author}</p>

            <div className="flex items-center gap-3 text-xs text-slate-400 mb-3">
              <span>📖 {book.pages} pages</span>
              {book.publication_year && <span>📅 {book.publication_year}</span>}
            </div>

            {/* Book DNA Attribute Pills */}
            <div className="mb-3">
              <BookDnaPills dna={book.book_dna} compact />
            </div>
          </div>
        </div>

        {/* Spoiler-Free AI Explanation */}
        {book.explanation && (
          <div className="mt-4 p-3 rounded-xl bg-slate-950/70 border border-indigo-500/20 text-xs text-slate-300 leading-relaxed">
            <div className="flex items-center gap-1.5 text-indigo-400 font-semibold mb-1">
              <ShieldAlert className="w-3.5 h-3.5 text-indigo-400" />
              <span>Spoiler-Free AI Reason</span>
            </div>
            <p>{book.explanation}</p>
          </div>
        )}

        {/* Verified Availability & Access Links ("Where to Get It") */}
        <BookAvailability availability={book.availability} />
      </div>

      {/* Action Controls */}
      <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <button
            disabled={loading}
            onClick={() => handleStatusUpdate("saved")}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg border transition-all ${
              status === "saved"
                ? "bg-indigo-600/30 border-indigo-500 text-indigo-300"
                : "bg-slate-800/60 border-slate-700/60 text-slate-300 hover:bg-slate-800"
            }`}
          >
            <Bookmark className="w-3.5 h-3.5 text-indigo-400" />
            <span>{status === "saved" ? "Saved" : "Save"}</span>
          </button>

          <button
            disabled={loading}
            onClick={() => handleStatusUpdate("read")}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg border transition-all ${
              status === "read"
                ? "bg-emerald-600/30 border-emerald-500 text-emerald-300"
                : "bg-slate-800/60 border-slate-700/60 text-slate-300 hover:bg-slate-800"
            }`}
          >
            <Check className="w-3.5 h-3.5 text-emerald-400" />
            <span>{status === "read" ? "Read" : "Mark Read"}</span>
          </button>
        </div>

        <button
          disabled={loading}
          onClick={() => handleStatusUpdate("rejected")}
          className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-950/40 transition-all ${
            status === "rejected" ? "text-rose-400" : ""
          }`}
          title="Don't recommend this book again"
        >
          <XCircle className="w-3.5 h-3.5" />
          <span>Dismiss</span>
        </button>
      </div>
    </div>
  );
};
