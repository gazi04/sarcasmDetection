import axios from 'axios';
import type {
  TrainingResponse,
  PredictionResponse,
  AnalysisResponse,
  ApiStatus
} from '@/types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const apiService = {
  async trainModels(): Promise<TrainingResponse> {
    const response = await api.post<TrainingResponse>('/train', {});
    return response.data;
  },

  async predictHeadline(headline: string): Promise<PredictionResponse> {
    const response = await api.post<PredictionResponse>('/predict', {
      headline
    });
    return response.data;
  },

  async analyzeDataset(): Promise<AnalysisResponse> {
    const response = await api.get<AnalysisResponse>('/analyze');
    return response.data;
  },

  async getStatus(): Promise<ApiStatus> {
    const response = await api.get<ApiStatus>('/status');
    return response.data;
  }
};
