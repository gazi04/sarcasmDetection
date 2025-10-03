<template>
  <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
    <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
      🔮 Predict Sarcasm
    </h2>

    <!-- Input Form -->
    <div class="mb-6">
      <div class="flex gap-4">
        <input
          v-model="headlineInput"
          @keyup.enter="handlePredict"
          placeholder="Enter a headline to analyze for sarcasm..."
          class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
        />
        <button
          @click="handlePredict"
          :disabled="!headlineInput.trim()"
          class="btn-predict"
          :class="{ 'opacity-50 cursor-not-allowed': !headlineInput.trim() }"
        >
          Analyze
        </button>
      </div>
    </div>

    <!-- Prediction Results -->
    <div v-if="predictionResult" class="mt-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Prediction Results</h3>

      <!-- Original Headline -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <h4 class="font-semibold text-gray-700 mb-2">Headline:</h4>
        <p class="text-gray-800 text-lg">"{{ predictionResult.headline }}"</p>
      </div>

      <!-- Model Predictions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="prediction in predictionResult.predictions"
          :key="prediction.model_type"
          class="prediction-card"
          :class="prediction.is_sarcastic ? 'border-red-200 bg-red-50' : 'border-green-200 bg-green-50'"
        >
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-bold text-gray-800 text-lg">{{ prediction.model_name }}</h4>
            <span
              class="px-3 py-1 rounded-full text-sm font-semibold"
              :class="prediction.is_sarcastic ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'"
            >
              {{ prediction.prediction }}
            </span>
          </div>

          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-1">
              <span>Confidence:</span>
              <span class="font-semibold">{{ (prediction.confidence * 100).toFixed(1) }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-500"
                :class="prediction.is_sarcastic ? 'bg-red-500' : 'bg-green-500'"
                :style="{ width: (prediction.confidence * 100) + '%' }"
              ></div>
            </div>
          </div>

          <div class="text-center">
            <span
              class="text-4xl"
              :class="prediction.is_sarcastic ? 'text-red-500' : 'text-green-500'"
            >
              {{ prediction.is_sarcastic ? '😂' : '😊' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { PredictionResponse } from '@/types';

const headlineInput = ref('');
const emit = defineEmits<{
  predict: [headline: string];
}>();

const props = defineProps<{
  predictionResult: PredictionResponse | null;
}>();

const handlePredict = () => {
  if (headlineInput.value.trim()) {
    emit('predict', headlineInput.value.trim());
  }
};
</script>

