export interface TrainingResponse {
  status: string;
  message: string;
  model_comparison: ModelComparison[];
  best_model: string;
}

export interface ModelComparison {
  name: string;
  type: string;
  accuracy: number;
  test_set_size: number;
}

export interface PredictionResponse {
  headline: string;
  predictions: PredictionResult[];
}

export interface PredictionResult {
  model_name: string;
  model_type: string;
  prediction: string;
  is_sarcastic: boolean;
  confidence: number;
}

export interface AnalysisResponse {
  basic_statistics: BasicStatistics;
  word_frequencies: WordFrequencies;
  text_length_stats: TextLengthStats;
}

export interface BasicStatistics {
  total_samples: number;
  sarcastic_samples: number;
  non_sarcastic_samples: number;
  sarcastic_percentage: number;
  non_sarcastic_percentage: number;
  class_distribution: Record<string, number>;
}

export interface WordFrequencies {
  sarcastic: WordFrequency[];
  non_sarcastic: WordFrequency[];
}

export interface WordFrequency {
  word: string;
  frequency: number;
}

export interface TextLengthStats {
  average_words: AverageWords;
  length_range: LengthRange;
}

export interface AverageWords {
  sarcastic: number;
  non_sarcastic: number;
  overall: number;
}

export interface LengthRange {
  shortest: number;
  longest: number;
}

export interface ApiStatus {
  data_loaded: boolean;
  models_trained: boolean;
  data_samples: number;
}
