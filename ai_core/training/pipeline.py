from typing import List, Dict, Any

# from models import TrainingData, ModelResult
# from config import LogisticRegressionConfig, ModelConfig
# from model_trainers import LogisticRegressionTrainer, NaiveBayesTrainer
# from evaluator import ModelEvaluator, PredictionService
# from preproces import text_preprocessing

from ai_core.data.models import ModelResult, TrainingData
from ai_core.models.logistic_regression_trainer import LogisticRegressionTrainer
from ai_core.models.bayes_naive_trainer import NaiveBayesTrainer
from ai_core.config import ModelConfig, LogisticRegressionConfig
from ai_core.training.evaluator import ModelEvaluator, PredictionService
from ai_core.utils.preproces import text_preprocessing

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
            print(f"\nTraining {name.replace('_', ' ').title()}...")
            result = trainer.train(data)
            result = self.evaluator.evaluate_model(result)
            self.evaluator.plot_confusion_matrix(result)
            results[name] = result
        
        return results
    
    def run_predictions(self, model_results: Dict[str, ModelResult], test_texts: List[str]):
        print("\nTesting with sample predictions:")
        
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

