export interface BookDNA {
  mood: string;
  pacing: string;
  romance_level: string;
  complexity: string;
  emotional_intensity?: string;
  setting?: string;
  themes?: string;
}

export interface BookAvailability {
  id?: string;
  provider_name: string;
  provider_type: 'read_borrow' | 'buy' | string;
  url: string;
  is_verified?: boolean;
}

export interface Book {
  id: string;
  title: string;
  author: string;
  description?: string;
  pages: number;
  publication_year?: number;
  cover_url?: string;
  match_score?: number;
  explanation?: string;
  score_breakdown?: {
    semantic_similarity: number;
    constraint_satisfaction: number;
    book_dna_match: number;
    history_penalty: number;
  };
  book_dna: BookDNA;
  availability?: BookAvailability[];
}

export interface ExtractedPreferences {
  genre: string;
  subgenre?: string;
  mood: string;
  pacing: string;
  romance_level: string;
  complexity: string;
  max_pages?: number | null;
  explicit_constraints?: string[];
  themes?: string[];
}

export interface DiscoverResponse {
  session_id: string;
  original_query: string;
  extracted_preferences: ExtractedPreferences;
  recommendations: Book[];
}

export interface ComparisonData {
  active_intent: ExtractedPreferences;
  compared_books: Book[];
  analysis: {
    book_id: string;
    title: string;
    intent_alignment_score: number;
    strengths: string[];
  }[];
  verdict: string;
}

export interface ReadingPathStep {
  step: number;
  stage: string;
  book_id: string;
  title: string;
  author: string;
  pages: number;
  complexity: string;
  reason: string;
}

export interface ReadingPath {
  path_name: string;
  total_steps: number;
  steps: ReadingPathStep[];
}

export interface EvaluationExperiment {
  test_query: string;
  conventional_search: {
    results_count: number;
    precision_at_5: number;
    top_titles: string[];
  };
  natural_language_search: {
    extracted_intent: ExtractedPreferences;
    results_count: number;
    precision_at_5: number;
    top_titles: string[];
    top_scores: number[];
  };
  findings: string;
}
