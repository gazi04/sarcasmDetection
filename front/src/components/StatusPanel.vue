<template>
  <div class="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
    <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
      📈 System Status
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <!-- Data Status -->
      <div class="status-card" :class="status?.data_loaded ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'">
        <div class="text-3xl mb-2">{{ status?.data_loaded ? '📁' : '📭' }}</div>
        <h3 class="font-semibold text-gray-800">Data Loaded</h3>
        <p class="text-sm text-gray-600">
          {{ status?.data_loaded ? `${status.data_samples} samples` : 'No data' }}
        </p>
      </div>

      <!-- Models Status -->
      <div class="status-card" :class="status?.models_trained ? 'bg-green-50 border-green-200' : 'bg-yellow-50 border-yellow-200'">
        <div class="text-3xl mb-2">{{ status?.models_trained ? '🤖' : '⏳' }}</div>
        <h3 class="font-semibold text-gray-800">Models Trained</h3>
        <p class="text-sm text-gray-600">
          {{ status?.models_trained ? 'Ready for prediction' : 'Not trained' }}
        </p>
      </div>

      <!-- Best Model -->
      <div class="status-card bg-blue-50 border-blue-200" v-if="trainingResult">
        <div class="text-3xl mb-2">🏆</div>
        <h3 class="font-semibold text-gray-800">Best Model</h3>
        <p class="text-sm text-gray-600">{{ trainingResult.best_model }}</p>
      </div>
    </div>

    <!-- Model Comparison Table -->
    <div v-if="trainingResult" class="mt-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Model Performance</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full bg-white rounded-lg overflow-hidden">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Model</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Accuracy</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Test Samples</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="model in trainingResult.model_comparison" :key="model.type">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <span class="text-xl mr-3">🤖</span>
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ model.name }}</div>
                    <div class="text-sm text-gray-500">{{ model.type }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                  :class="model.accuracy > 0.8 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'">
                  {{ (model.accuracy * 100).toFixed(1) }}%
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ model.test_set_size.toLocaleString() }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  ✅ Trained
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ApiStatus, TrainingResponse } from '@/types';

defineProps<{
  status: ApiStatus | null;
  trainingResult: TrainingResponse | null;
}>();
</script>

