<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <header class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-800 mb-4 font-aller">
        🤖 Sarcasm Detection Dashboard
      </h1>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto">
        AI-powered sarcasm detection using machine learning models
      </p>
    </header>

    <!-- Action Buttons -->
    <div class="flex flex-wrap justify-center gap-4 mb-12">
      <button
        @click="trainModels"
        :disabled="loading"
        class="btn-primary"
        :class="{ 'opacity-50 cursor-not-allowed': loading }"
      >
        🚀 Train Models
      </button>

      <button
        @click="analyzeDataset"
        :disabled="loading"
        class="btn-secondary"
        :class="{ 'opacity-50 cursor-not-allowed': loading }"
      >
        📊 Analyze Dataset
      </button>

      <button
        @click="showPrediction = !showPrediction"
        class="btn-accent"
      >
        🔮 Predict Sarcasm
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-flex items-center px-6 py-3 bg-blue-100 text-blue-700 rounded-lg">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-700 mr-3"></div>
        Processing...
      </div>
    </div>

    <!-- Status Panel -->
    <StatusPanel
      :status="status"
      :training-result="trainingResult"
      class="mb-8"
    />

    <!-- Prediction Panel -->
    <PredictionPanel
      v-if="showPrediction"
      @predict="predictHeadline"
      :prediction-result="predictionResult"
      class="mb-8"
    />

    <!-- Analysis Panel -->
    <AnalysisPanel
      v-if="analysisData"
      :analysis-data="analysisData"
      class="mb-8"
    />

    <!-- Error Message -->
    <div v-if="error" class="fixed top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg shadow-lg max-w-md">
      <div class="flex items-center">
        <span class="text-xl mr-2">⚠️</span>
        <span class="font-semibold">{{ error }}</span>
        <button @click="error = ''" class="ml-auto text-red-700 hover:text-red-900">
          ✕
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { apiService } from '@/services/api';
import type {
  TrainingResponse,
  PredictionResponse,
  AnalysisResponse,
  ApiStatus
} from '@/types';

import StatusPanel from './StatusPanel.vue';
import PredictionPanel from './PredictionPanel.vue';
import AnalysisPanel from './AnalysisPanel.vue';

const loading = ref(false);
const error = ref('');
const showPrediction = ref(false);
const status = ref<ApiStatus | null>(null);
const trainingResult = ref<TrainingResponse | null>(null);
const predictionResult = ref<PredictionResponse | null>(null);
const analysisData = ref<AnalysisResponse | null>(null);

const loadStatus = async () => {
  try {
    status.value = await apiService.getStatus();
  } catch (err) {
    console.error('Failed to load status:', err);
  }
};

const trainModels = async () => {
  loading.value = true;
  error.value = '';
  try {
    trainingResult.value = await apiService.trainModels();
    await loadStatus(); // Refresh status after training
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Training failed';
  } finally {
    loading.value = false;
  }
};

const analyzeDataset = async () => {
  loading.value = true;
  error.value = '';
  try {
    analysisData.value = await apiService.analyzeDataset();
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Analysis failed';
  } finally {
    loading.value = false;
  }
};

const predictHeadline = async (headline: string) => {
  loading.value = true;
  error.value = '';
  try {
    predictionResult.value = await apiService.predictHeadline(headline);
    showPrediction.value = true;
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Prediction failed';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadStatus();
});
</script>

