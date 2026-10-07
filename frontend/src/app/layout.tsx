import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LitLens - AI-Driven Natural Language Book Discovery & Recommendation",
  description: "Discover books using natural language reading intents, structured Book DNA, transparent hybrid ranking, conversational refinement, and preference-aware comparison.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased bg-slate-950 text-slate-100">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
