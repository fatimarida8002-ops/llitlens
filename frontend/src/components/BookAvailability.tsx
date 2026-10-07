"use client";

import React from "react";
import { BookAvailability as AvailabilityType } from "@/types";
import { ExternalLink, BookOpen, ShoppingBag, ShoppingCart } from "lucide-react";

interface BookAvailabilityProps {
  availability?: AvailabilityType[];
}

export const BookAvailability: React.FC<BookAvailabilityProps> = ({ availability }) => {
  const verifiedList = (availability || []).filter((a) => a.url);

  if (verifiedList.length === 0) {
    return (
      <div className="mt-3 pt-3 border-t border-slate-800/60">
        <span className="text-[11px] font-semibold text-slate-400 block mb-1">
          Where to Get It
        </span>
        <p className="text-[11px] text-slate-500 italic">
          Availability links could not be verified for this book.
        </p>
      </div>
    );
  }

  const getProviderBadge = (provider: string, type: string) => {
    if (provider.toLowerCase().includes("open library")) {
      return {
        label: "Read / Borrow",
        provider: "Open Library",
        colorClass: "bg-amber-950/80 hover:bg-amber-900 border-amber-500/40 text-amber-200",
        icon: <BookOpen className="w-3.5 h-3.5 text-amber-400 shrink-0" />
      };
    }
    if (provider.toLowerCase().includes("google")) {
      return {
        label: "Google Books",
        provider: "Google Books",
        colorClass: "bg-blue-950/80 hover:bg-blue-900 border-blue-500/40 text-blue-200",
        icon: <ShoppingBag className="w-3.5 h-3.5 text-blue-400 shrink-0" />
      };
    }
    if (provider.toLowerCase().includes("amazon")) {
      return {
        label: "Amazon",
        provider: "Amazon",
        colorClass: "bg-orange-950/80 hover:bg-orange-900 border-orange-500/40 text-orange-200",
        icon: <ShoppingCart className="w-3.5 h-3.5 text-orange-400 shrink-0" />
      };
    }
    return {
      label: type === "read_borrow" ? "Read / Borrow" : "Buy",
      provider: provider,
      colorClass: "bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200",
      icon: <ExternalLink className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
    };
  };

  return (
    <div className="mt-3 pt-3 border-t border-slate-800/80">
      <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider block mb-2">
        Where to Get It
      </span>
      <div className="flex flex-wrap gap-2">
        {verifiedList.map((item, idx) => {
          const info = getProviderBadge(item.provider_name, item.provider_type);
          return (
            <a
              key={idx}
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold border transition-all ${info.colorClass}`}
              title={`Open ${info.provider} in a new tab`}
            >
              {info.icon}
              <span>{info.provider}</span>
              <ExternalLink className="w-3 h-3 opacity-60 ml-0.5" />
            </a>
          );
        })}
      </div>
    </div>
  );
};
