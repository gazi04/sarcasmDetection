<template>
  <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
    <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
      📊 Dataset Analysis
    </h2>

    <!-- Basic Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="stat-card bg-blue-50 border-blue-200">
        <div class="text-2xl mb-2">📈</div>
        <h3 class="font-semibold text-gray-800">Total Samples</h3>
        <p class="text-2xl font-bold text-blue-600">{{ analysisData.basic_statistics.total_samples.toLocaleString() }}</p>
      </div>

      <div class="stat-card bg-green-50 border-green-200">
        <div class="text-2xl mb-2">😊</div>
        <h3 class="font-semibold text-gray-800">Non-Sarcastic</h3>
        <p class="text-2xl font-bold text-green-600">
          {{ (analysisData.basic_statistics.non_sarcastic_percentage * 100).toFixed(1) }}%
        </p>
        <p class="text-sm text-gray-600">{{ analysisData.basic_statistics.non_sarcastic_samples.toLocaleString() }} samples</p>
      </div>

      <div class="stat-card bg-red-50 border-red-200">
        <div class="text-2xl mb-2">😂</div>
        <h3 class="font-semibold text-gray-800">Sarcastic</h3>
        <p class="text-2xl font-bold text-red-600">
          {{ (analysisData.basic_statistics.sarcastic_percentage * 100).toFixed(1) }}%
        </p>
        <p class="text-sm text-gray-600">{{ analysisData.basic_statistics.sarcastic_samples.toLocaleString() }} samples</p>
      </div>

      <div class="stat-card bg-purple-50 border-purple-200">
        <div class="text-2xl mb-2">📏</div>
        <h3 class="font-semibold text-gray-800">Avg Words</h3>
        <p class="text-2xl font-bold text-purple-600">{{ analysisData.text_length_stats.average_words.overall.toFixed(1) }}</p>
        <p class="text-sm text-gray-600">per headline</p>
      </div>
    </div>

    <!-- Word Frequencies -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
      <!-- Sarcastic Words -->
      <div class="word-frequency-card bg-red-50 border-red-200">
        <h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center">
          <span class="text-2xl mr-2">😂</span>
          Top Sarcastic Words
        </h3>
        <div class="space-y-2">
          <div
            v-for="(word, index) in analysisData.word_frequencies.sarcastic.slice(0, 10)"
            :key="word.word"
            class="flex items-center justify-between p-3 bg-white rounded-lg border border-red-100"
          >
            <div class="flex items-center">
              <span class="w-6 h-6 bg-red-500 text-white rounded-full text-xs flex items-center justify-center mr-3">
                {{ index + 1 }}
              </span>
              <span class="font-medium text-gray-800">{{ word.word }}</span>
            </div>
            <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-sm font-semibold">
              {{ word.frequency }}
            </span>
          </div>
        </div>
      </div>

      <!-- Non-Sarcastic Words -->
      <div class="word-frequency-card bg-green-50 border-green-200">
        <h3 class="text-xl font-semibold text-gray-800 mb-4 flex items-center">
          <span class="text-2xl mr-2">😊</span>
          Top Non-Sarcastic Words
        </h3>
        <div class="space-y-2">
          <div
            v-for="(word, index) in analysisData.word_frequencies.non_sarcastic.slice(0, 10)"
            :key="word.word"
            class="flex items-center justify-between p-3 bg-white rounded-lg border border-green-100"
          >
            <div class="flex items-center">
              <span class="w-6 h-6 bg-green-500 text-white rounded-full text-xs flex items-center justify-center mr-3">
                {{ index + 1 }}
              </span>
              <span class="font-medium text-gray-800">{{ word.word }}</span>
            </div>
            <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-semibold">
              {{ word.frequency }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Text Length Statistics -->
    <div class="bg-gray-50 rounded-lg p-6 border border-gray-200">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">📏 Text Length Analysis</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center">
          <div class="text-3xl font-bold text-blue-600 mb-2">
            {{ analysisData.text_length_stats.average_words.sarcastic.toFixed(1) }}
          </div>
          <div class="text-sm text-gray-600">Avg Sarcastic Words</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-green-600 mb-2">
            {{ analysisData.text_length_stats.average_words.non_sarcastic.toFixed(1) }}
          </div>
          <div class="text-sm text-gray-600">Avg Non-Sarcastic Words</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-purple-600 mb-2">
            {{ analysisData.text_length_stats.length_range.shortest }} - {{ analysisData.text_length_stats.length_range.longest }}
          </div>
          <div class="text-sm text-gray-600">Word Range</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AnalysisResponse } from '@/types';

defineProps<{
  analysisData: AnalysisResponse;
}>();
</script>

