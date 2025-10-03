<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue';
import axios from 'axios';
import { Bar, Pie } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';
import { ArrowPathIcon, ChartBarIcon, CpuChipIcon, LightBulbIcon } from '@heroicons/vue/24/outline';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

// --- API Configuration ---
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Change this to your FastAPI server address
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- TypeScript Interfaces (from FastAPI schemas) ---
interface Status {
  data_loaded: boolean;
  models_trained: boolean;
  data_samples: number;
}

interface ModelComparison {
  name: str;
  type: str;
  accuracy: float;
  test_set_size: int;
}

interface TrainingResponse {
  status: str;
  message: str;
  model_comparison: ModelComparison[];
  best_model: string;
}

interface PredictionResult {
  model_name: string;
  model_type: string;
  prediction: string;
  is_sarcastic: boolean;
  confidence: number;
}

interface PredictionResponse {
  headline: string;
  predictions: PredictionResult[];
}

interface WordFrequency {
  word: string;
  frequency: number;
}

interface AnalysisResponse {
  basic_statistics: {
    total_samples: number;
    sarcastic_samples: number;
    non_sarcastic_samples: number;
    sarcastic_percentage: number;
    non_sarcastic_percentage: number;
    class_distribution: Record<string, number>;
  };
  word_frequencies: {
    sarcastic: WordFrequency[];
    non_sarcastic: WordFrequency[];
  };
  text_length_stats: {
    average_words: Record<string, number>;
    length_range: Record<string, number>;
  };
}

// --- Component State ---
const status = ref<Status | null>(null);
const analysisData = ref<AnalysisResponse | null>(null);
const trainingResults = ref<TrainingResponse | null>(null);
const predictionResults = ref<PredictionResponse | null>(null);
const headlineToPredict = ref<string>('');
const errorMessage = ref<string | null>(null);

const isLoading = reactive({
  status: false,
  train: false,
  analyze: false,
  predict: false,
});

// --- API Functions ---
const fetchStatus = async () => {
  isLoading.status = true;
  errorMessage.value = null;
  try {
    const { data } = await apiClient.get<Status>('/status');
    status.value = data;
  } catch (error: any) {
    errorMessage.value = `Failed to fetch status: ${error.response?.data?.detail || error.message}`;
  } finally {
    isLoading.status = false;
  }
};

const handleTrain = async () => {
  isLoading.train = true;
  errorMessage.value = null;
  trainingResults.value = null; // Clear previous results
  try {
    const { data } = await apiClient.post<TrainingResponse>('/train', {});
    trainingResults.value = data;
    await fetchStatus(); // Refresh status after training
  } catch (error: any) {
    errorMessage.value = `Training failed: ${error.response?.data?.detail || error.message}`;
  } finally {
    isLoading.train = false;
  }
};

const handleAnalyze = async () => {
  isLoading.analyze = true;
  errorMessage.value = null;
  analysisData.value = null; // Clear previous results
  try {
    const { data } = await apiClient.get<AnalysisResponse>('/analyze');
    analysisData.value = data;
  } catch (error: any) {
    errorMessage.value = `Analysis failed: ${error.response?.data?.detail || error.message}`;
  } finally {
    isLoading.analyze = false;
  }
};

const handlePredict = async () => {
  if (!headlineToPredict.value.trim()) {
    errorMessage.value = "Headline cannot be empty.";
    return;
  }
  isLoading.predict = true;
  errorMessage.value = null;
  predictionResults.value = null; // Clear previous results
  try {
    const { data } = await apiClient.post<PredictionResponse>('/predict', { headline: headlineToPredict.value });
    predictionResults.value = data;
  } catch (error: any) {
    errorMessage.value = `Prediction failed: ${error.response?.data?.detail || error.message}`;
  } finally {
    isLoading.predict = false;
  }
};

// --- Lifecycle Hook ---
onMounted(() => {
  fetchStatus();
});

// --- Chart Data & Options (Computed Properties) ---
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#D1D5DB', // text-gray-300
        font: {
          family: 'Lato, sans-serif',
          size: 14,
        }
      }
    }
  },
  scales: {
    y: {
      ticks: { color: '#9CA3AF' /* text-gray-400 */ },
      grid: { color: '#374151' /* border-gray-700 */ }
    },
    x: {
      ticks: { color: '#9CA3AF' /* text-gray-400 */ },
      grid: { color: '#374151' /* border-gray-700 */ }
    }
  }
};

const classDistributionChartData = computed(() => {
  if (!analysisData.value) return null;
  const stats = analysisData.value.basic_statistics;
  return {
    labels: ['Sarcastic', 'Non-Sarcastic'],
    datasets: [
      {
        backgroundColor: ['#F87171' /* red-400 */, '#4ADE80' /* green-400 */],
        data: [stats.sarcastic_samples, stats.non_sarcastic_samples],
      },
    ],
  };
});

const wordFrequencyChartData = computed(() => {
  if (!analysisData.value) return null;
  const sarcasticWords = analysisData.value.word_frequencies.sarcastic.slice(0, 10);
  const nonSarcasticWords = analysisData.value.word_frequencies.non_sarcastic.slice(0, 10);

  // Use a common set of words for better comparison if desired, here we just show top 10 for each
  const labels = sarcasticWords.map(w => w.word);

  return {
    labels: labels,
    datasets: [
      {
        label: 'Sarcastic Word Frequency',
        backgroundColor: '#F87171', // red-400
        data: sarcasticWords.map(w => w.frequency),
      },
      {
        label: 'Non-Sarcastic Word Frequency',
        backgroundColor: '#4ADE80', // green-400
        data: nonSarcasticWords.map(w => w.frequency),
      },
    ],
  };
});
</script>

<template>
  <div class="bg-gray-900 text-gray-200 min-h-screen font-sans p-4 sm:p-6 lg:p-8">
    <div class="max-w-7xl mx-auto">

      <header class="mb-8 border-b border-gray-700 pb-4">
        <h1 class="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
          <CpuChipIcon class="h-10 w-10 text-cyan-400" />
          Sarcasm Detection Dashboard
        </h1>
        <p class="text-gray-400 mt-2">A simple interface to train, analyze, and predict sarcasm in text headlines.</p>
      </header>

      <div v-if="errorMessage" class="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-lg relative mb-6" role="alert">
        <strong class="font-bold">Error: </strong>
        <span class="block sm:inline">{{ errorMessage }}</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <div class="lg:col-span-1 flex flex-col gap-8">

          <div class="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 class="text-2xl font-bold text-white mb-6">Controls</h2>
            <div class="flex flex-col gap-4">
              <button @click="handleTrain" :disabled="isLoading.train || !status?.data_loaded" class="flex items-center justify-center w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg shadow-md transition-transform transform hover:scale-105">
                <ArrowPathIcon v-if="isLoading.train" class="animate-spin h-5 w-5 mr-3" />
                <CpuChipIcon v-else class="h-6 w-6 mr-3" />
                {{ isLoading.train ? 'Training...' : 'Train Models' }}
              </button>

              <button @click="handleAnalyze" :disabled="isLoading.analyze || !status?.data_loaded" class="flex items-center justify-center w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg shadow-md transition-transform transform hover:scale-105">
                 <ArrowPathIcon v-if="isLoading.analyze" class="animate-spin h-5 w-5 mr-3" />
                <ChartBarIcon v-else class="h-6 w-6 mr-3" />
                {{ isLoading.analyze ? 'Analyzing...' : 'Analyze Dataset' }}
              </button>
            </div>
          </div>

          <div class="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 class="text-2xl font-bold text-white mb-6">Predict</h2>
            <div class="flex flex-col gap-4">
              <input type="text" v-model="headlineToPredict" placeholder="Enter a headline to predict..." class="w-full bg-gray-700 border border-gray-600 text-gray-200 placeholder-gray-400 rounded-lg p-3 focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 outline-none transition" />
              <button @click="handlePredict" :disabled="isLoading.predict || !status?.models_trained" class="flex items-center justify-center w-full bg-cyan-600 hover:bg-cyan-500 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg shadow-md transition-transform transform hover:scale-105">
                <ArrowPathIcon v-if="isLoading.predict" class="animate-spin h-5 w-5 mr-3" />
                <LightBulbIcon v-else class="h-6 w-6 mr-3" />
                {{ isLoading.predict ? 'Predicting...' : 'Predict' }}
              </button>
            </div>
          </div>

           <div class="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 class="text-2xl font-bold text-white mb-4">API Status</h2>
            <div v-if="status" class="space-y-3 text-lg">
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Dataset Loaded:</span>
                <span :class="status.data_loaded ? 'text-green-400' : 'text-red-400'" class="font-bold">{{ status.data_loaded ? 'Yes' : 'No' }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Models Trained:</span>
                <span :class="status.models_trained ? 'text-green-400' : 'text-red-400'" class="font-bold">{{ status.models_trained ? 'Yes' : 'No' }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-400">Data Samples:</span>
                <span class="font-bold text-cyan-400">{{ status.data_samples.toLocaleString() }}</span>
              </div>
            </div>
             <div v-else class="text-gray-400">
                Loading status...
              </div>
          </div>

        </div>

        <div class="lg:col-span-2 flex flex-col gap-8">

          <div v-if="predictionResults" class="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 class="text-2xl font-bold text-white mb-4">Prediction Result</h2>
            <p class="text-gray-400 mb-2">Headline:</p>
            <p class="text-cyan-300 text-lg font-semibold bg-gray-900/50 p-3 rounded-lg mb-6">"{{ predictionResults.headline }}"</p>
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead class="bg-gray-700/50">
                  <tr>
                    <th class="p-3">Model</th>
                    <th class="p-3">Type</th>
                    <th class="p-3">Prediction</th>
                    <th class="p-3">Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="pred in predictionResults.predictions" :key="pred.model_name" class="border-b border-gray-700">
                    <td class="p-3 font-semibold">{{ pred.model_name }}</td>
                    <td class="p-3 text-gray-400">{{ pred.model_type }}</td>
                    <td class="p-3 font-bold" :class="pred.is_sarcastic ? 'text-red-400' : 'text-green-400'">
                      {{ pred.prediction }}
                    </td>
                    <td class="p-3 font-mono text-cyan-300">{{ (pred.confidence * 100).toFixed(2) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="trainingResults" class="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 class="text-2xl font-bold text-white mb-4">{{ trainingResults.message }}</h2>
            <p class="text-gray-400 mb-4">Best performing model: <span class="font-bold text-emerald-400">{{ trainingResults.best_model }}</span></p>
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead class="bg-gray-700/50">
                  <tr>
                    <th class="p-3">Model Name</th>
                    <th class="p-3">Type</th>
                    <th class="p-3">Accuracy</th>
                    <th class="p-3">Test Set Size</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="model in trainingResults.model_comparison" :key="model.name" class="border-b border-gray-700" :class="{ 'bg-emerald-500/10': model.name === trainingResults.best_model }">
                    <td class="p-3 font-semibold">{{ model.name }}</td>
                    <td class="p-3 text-gray-400">{{ model.type }}</td>
                    <td class="p-3 font-mono text-cyan-300">{{ (model.accuracy * 100).toFixed(2) }}%</td>
                    <td class="p-3 text-gray-400">{{ model.test_set_size }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-if="analysisData" class="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h2 class="text-2xl font-bold text-white mb-6">Dataset Analysis</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div class="h-80">
                <h3 class="text-xl font-bold text-white mb-4 text-center">Class Distribution</h3>
                <Pie v-if="classDistributionChartData" :data="classDistributionChartData" :options="chartOptions" />
              </div>
              <div class="h-80">
                <h3 class="text-xl font-bold text-white mb-4 text-center">Top 10 Word Frequencies</h3>
                <Bar v-if="wordFrequencyChartData" :data="wordFrequencyChartData" :options="chartOptions" />
              </div>
            </div>
          </div>

          <div v-if="!trainingResults && !analysisData && !predictionResults" class="bg-gray-800/50 border-2 border-dashed border-gray-700 p-10 rounded-xl text-center flex flex-col items-center justify-center h-full">
            <img src="https://raw.githubusercontent.com/google/material-design-icons/master/png/action/analytics/materialicons/48dp/2x/baseline_analytics_white_48dp.png" alt="Analytics Icon" class="h-16 w-16 mb-4 opacity-30" />
            <h3 class="text-xl font-bold text-gray-300">Your results will appear here.</h3>
            <p class="text-gray-400 mt-2">Click 'Train' or 'Analyze' to get started, or 'Predict' after training a model.</p>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>
