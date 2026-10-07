import { DiscoverResponse, ComparisonData, ReadingPath, EvaluationExperiment } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function discoverBooks(query: string): Promise<DiscoverResponse> {
  const res = await fetch(`${API_BASE_URL}/discover`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to discover books.");
  }
  return res.json();
}

export async function refineRecommendations(sessionId: string, instruction: string) {
  const res = await fetch(`${API_BASE_URL}/refine`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, instruction }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to refine recommendations.");
  }
  return res.json();
}

export async function compareBooks(bookIds: string[], activeIntent: any): Promise<ComparisonData> {
  const res = await fetch(`${API_BASE_URL}/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_ids: bookIds, active_intent: activeIntent }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to compare books.");
  }
  return res.json();
}

export async function updateBookStatus(bookId: string, status: string) {
  const res = await fetch(`${API_BASE_URL}/books/${bookId}/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ book_id: bookId, status }),
  });
  if (!res.ok) throw new Error("Failed to update book status.");
  return res.json();
}

export async function getUserHistory() {
  const res = await fetch(`${API_BASE_URL}/history`);
  if (!res.ok) throw new Error("Failed to fetch reading history.");
  return res.json();
}

export async function getReadingPath(topic: string = "Fantasy"): Promise<ReadingPath> {
  const res = await fetch(`${API_BASE_URL}/reading-path`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic_or_genre: topic }),
  });
  if (!res.ok) throw new Error("Failed to generate reading path.");
  return res.json();
}

export async function getEvaluationExperiment(): Promise<EvaluationExperiment> {
  const res = await fetch(`${API_BASE_URL}/evaluation/experiment`);
  if (!res.ok) throw new Error("Failed to fetch evaluation experiment.");
  return res.json();
}
