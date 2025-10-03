"""
End-to-end pipeline that prepares data, trains models, evaluates, and predicts.

This class orchestrates preprocessing, training both Logistic Regression and
Naive Bayes models, evaluating them, generating artifacts, and providing
helpers to expose comparable results and predictions to the API layer.
"""

from ai_core.data.models import ModelResult, TrainingData
from ai_core.models.logistic_regression_trainer import LogisticRegressionTrainer
from ai_core.models.bayes_naive_trainer import NaiveBayesTrainer
from ai_core.config import ModelConfig, LogisticRegressionConfig
from ai_core.training.evaluator import ModelEvaluator, PredictionService
from ai_core.utils.preproces import text_preprocessing
from typing import List, Dict, Any

class SarcasmDetectionPipeline:
    def __init__(self):
        self.lr_config = LogisticRegressionConfig()
        self.nb_config = ModelConfig()
        self.evaluator = ModelEvaluator()
        self.prediction_service = PredictionService(text_preprocessing)
        
        self.trainers = {
            "logistic_regression": LogisticRegressionTrainer(self.lr_config),
            "naive_bayes": NaiveBayesTrainer(self.nb_config)
        }

    def prepare_data(self, raw_data: List[Dict[str, Any]]) -> TrainingData:
        headlines = []
        labels = []
        
        for item in raw_data:
            processed_text = text_preprocessing(item["headline"])
            headlines.append(processed_text)
            labels.append(item["is_sarcastic"])
        
        return TrainingData(headlines=headlines, labels=labels)
    
    def train_models(self, data: TrainingData) -> Dict[str, ModelResult]:
        results = {}
        
        for name, trainer in self.trainers.items():
            print("\n" + "="*50)
            print(f"TRAINING {name.replace('_', ' ').title()}...")
            print("="*50)
            result = trainer.train(data)
            result = self.evaluator.evaluate_model(result)
            self.evaluator.plot_confusion_matrix(result)
            results[name] = result
        
        return results
    
    def run_predictions(self, model_results: Dict[str, ModelResult], test_texts: List[str]):
        print("\n" + "="*50)
        print("TESTING WITH SAMPLE PREDICTIONS:")
        print("="*50)
        
        for text in test_texts:
            print(f"\n--- Testing: '{text}' ---")
            for model_name, result in model_results.items():
                prediction = self.prediction_service.predict_sarcasm(result, text)
                print(f"{result.model_name}:")
                self.prediction_service.print_prediction(prediction)
    
    def print_summary(self, model_results: Dict[str, ModelResult]):
        print("\n" + "="*50)
        print("TRAINING SUMMARY")
        print("="*50)
        
        for name, result in model_results.items():
            print(f"{result.model_name}: {result.accuracy:.2%} accuracy")
        
        best_model = max(model_results.values(), key=lambda x: x.accuracy)
        print(f"\nBest Model: {best_model.model_name} ({best_model.accuracy:.2%})")

    def data_analysis(self, data: TrainingData) -> None:
            print("\n" + "="*50)
            print("EXPLORATORY ANALYSIS")
            print("="*50)
            
            self._show_basic_statistics(data)
            
            self._show_word_frequencies(data)
            
            self._show_text_length_stats(data)

    def _show_basic_statistics(self, data: TrainingData) -> None:
        print("\nBASIC STATISTICS:")
        print(f"\t• Total samples: {len(data.headlines):,}")
        print(f"\t• Sarcastic samples: {sum(data.labels):,} ({sum(data.labels)/len(data.labels):.1%})")
        print(f"\t• Non-sarcastic samples: {len(data.labels)-sum(data.labels):,} ({(len(data.labels)-sum(data.labels))/len(data.labels):.1%})")
        
        distribution = data.get_class_distribution()
        print(f"\t• Class distribution: {distribution}")

    def _show_word_frequencies(self, data: TrainingData, top_n: int = 15) -> None:
        print(f"\nMOST FREQUENT WORDS (Top {top_n}):")
        
        sarcastic_texts = [text for text, label in zip(data.headlines, data.labels) if label == 1]
        non_sarcastic_texts = [text for text, label in zip(data.headlines, data.labels) if label == 0]
        
        sarcastic_words = self._get_word_frequencies(sarcastic_texts, top_n)
        non_sarcastic_words = self._get_word_frequencies(non_sarcastic_texts, top_n)
        
        print("Sarcastic headlines:")
        for i, (word, freq) in enumerate(sarcastic_words, 1):
            print(f"      {i:2d}. {word:<15} ({freq} occurrences)")
        
        print(f"Non-sarcastic headlines:")
        for i, (word, freq) in enumerate(non_sarcastic_words, 1):
            print(f"      {i:2d}. {word:<15} ({freq} occurrences)")

    def _get_word_frequencies(self, texts: List[str], top_n: int) -> List[tuple]:
        from collections import Counter
        import re
        
        all_words = []
        for text in texts:
            words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower()) # Words with 2+ letters
            all_words.extend(words)
        
        word_freq = Counter(all_words)
        return word_freq.most_common(top_n)

    def _show_text_length_stats(self, data: TrainingData) -> None:
        print("\nTEXT LENGTH STATISTICS:")
        
        sarcastic_lengths = [len(text.split()) for text, label in zip(data.headlines, data.labels) if label == 1]
        non_sarcastic_lengths = [len(text.split()) for text, label in zip(data.headlines, data.labels) if label == 0]
        
        print("\t• Average words per headline:")
        print(f"\t\t- Sarcastic: {sum(sarcastic_lengths)/len(sarcastic_lengths):.1f} words")
        print(f"\t\t- Non-sarcastic: {sum(non_sarcastic_lengths)/len(non_sarcastic_lengths):.1f} words")
        print(f"\t\t- Overall: {sum(len(text.split()) for text in data.headlines)/len(data.headlines):.1f} words")
        
        print("\t• Headline length range:")
        print(f"\t\t- Shortest: {min(len(text.split()) for text in data.headlines)} words")
        print(f"\t\t- Longest: {max(len(text.split()) for text in data.headlines)} words")

    # =======================================================================
    #     METHODS USED FOR THE API CORE 
    # =======================================================================

    def get_training_comparison(self, model_results: Dict[str, ModelResult]) -> Dict[str, Any]:
        comparison = {
            "models": [],
            "best_model": "",
            "best_accuracy": 0.0
        }
        
        for name, result in model_results.items():
            model_data = {
                "name": result.model_name,
                "type": name,
                "accuracy": float(result.accuracy),
                "test_set_size": len(result.y_test)
            }
            comparison["models"].append(model_data)
            
            if result.accuracy > comparison["best_accuracy"]:
                comparison["best_accuracy"] = float(result.accuracy)
                comparison["best_model"] = result.model_name
        
        return comparison

    def get_predictions(self, model_results: Dict[str, ModelResult], headline: str) -> Dict[str, Any]:
        predictions = {
            "headline": headline,
            "predictions": []
        }
        
        for name, result in model_results.items():
            prediction_result = self.prediction_service.predict_sarcasm(result, headline)
            
            prediction_data = {
                "model_name": result.model_name,
                "model_type": name,
                "prediction": prediction_result.prediction_label,
                "is_sarcastic": bool(prediction_result.is_sarcastic),
                "confidence": float(prediction_result.confidence)
            }
            predictions["predictions"].append(prediction_data)
        
        return predictions

    def get_analysis_data(self, data: TrainingData) -> Dict[str, Any]:
        total_samples = len(data.headlines)
        sarcastic_count = sum(data.labels)
        non_sarcastic_count = total_samples - sarcastic_count
        
        class_distribution = data.get_class_distribution()
        class_distribution_str = {str(key): value for key, value in class_distribution.items()}
        
        basic_stats = {
            "total_samples": total_samples,
            "sarcastic_samples": sarcastic_count,
            "non_sarcastic_samples": non_sarcastic_count,
            "sarcastic_percentage": float(sarcastic_count / total_samples),
            "non_sarcastic_percentage": float(non_sarcastic_count / total_samples),
            "class_distribution": class_distribution_str
        }
        
        sarcastic_texts = [text for text, label in zip(data.headlines, data.labels) if label == 1]
        non_sarcastic_texts = [text for text, label in zip(data.headlines, data.labels) if label == 0]
        
        word_frequencies = {
            "sarcastic": [{"word": word, "frequency": freq} for word, freq in self._get_word_frequencies(sarcastic_texts, 10)],
            "non_sarcastic": [{"word": word, "frequency": freq} for word, freq in self._get_word_frequencies(non_sarcastic_texts, 10)]
        }
        
        sarcastic_lengths = [len(text.split()) for text, label in zip(data.headlines, data.labels) if label == 1]
        non_sarcastic_lengths = [len(text.split()) for text, label in zip(data.headlines, data.labels) if label == 0]
        
        text_stats = {
            "average_words": {
                "sarcastic": float(sum(sarcastic_lengths) / len(sarcastic_lengths)) if sarcastic_lengths else 0,
                "non_sarcastic": float(sum(non_sarcastic_lengths) / len(non_sarcastic_lengths)) if non_sarcastic_lengths else 0,
                "overall": float(sum(len(text.split()) for text in data.headlines) / len(data.headlines))
            },
            "length_range": {
                "shortest": min(len(text.split()) for text in data.headlines),
                "longest": max(len(text.split()) for text in data.headlines)
            }
        }
        
        return {
            "basic_statistics": basic_stats,
            "word_frequencies": word_frequencies,
            "text_length_stats": text_stats
        }
