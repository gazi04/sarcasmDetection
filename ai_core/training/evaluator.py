from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

from ai_core.data.models import ModelResult, PredictionResult
from ai_core.config import PathConfig, Constants

class ModelEvaluator:
    def __init__(self, path_config: PathConfig = PathConfig()):
        self.path_config = path_config
    
    def _print_evaluation_results(self, result: ModelResult):
        print(f"\n{result.model_name} Evaluation Results:")
        print(f"Accuracy: {result.accuracy:.4f}")
        print("Detailed Classification Report:")
        print(
            classification_report(
                result.y_test, 
                result.predictions, 
                target_names=Constants.CLASS_NAMES
            )
        )
    
    def evaluate_model(self, result: ModelResult) -> ModelResult:
        accuracy = accuracy_score(result.y_test, result.predictions)
        result.accuracy = accuracy
        
        self._print_evaluation_results(result)
        return result
    
    def plot_confusion_matrix(self, result: ModelResult) -> None:
        cm = confusion_matrix(result.y_test, result.predictions)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=Constants.CLASS_NAMES,
            yticklabels=Constants.CLASS_NAMES,
        )
        plt.title(f"Confusion Matrix - {result.model_name}")
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.tight_layout()

        if not os.path.isdir(self.path_config.model_save_path):
           os.mkdir(self.path_config.model_save_path) 
        
        filename = f"{self.path_config.model_save_path}{self.path_config.confusion_matrix_path}_{result.model_name.lower().replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        print(f"Confusion matrix saved as '{filename}'")
        plt.close()

class PredictionService:
    def __init__(self, preprocessor):
        self.preprocessor = preprocessor
    
    def predict_sarcasm(self, model_result: ModelResult, text: str) -> PredictionResult:
        processed_text = self.preprocessor(text)
        features = model_result.vectorizer.transform([processed_text])
        prediction = model_result.model.predict(features)[0]
        probability = model_result.model.predict_proba(features)[0]
        
        confidence = probability[prediction]
        is_sarcastic = prediction == Constants.POSITIVE_CLASS
        
        return PredictionResult(
            text=text,
            prediction=prediction,
            confidence=confidence,
            is_sarcastic=is_sarcastic
        )
    
    def print_prediction(self, prediction: PredictionResult):
        print(f"\tHeadline: '{prediction.text}'")
        print(f"\tPrediction: {prediction.prediction_label}")
        print(f"\tConfidence: {prediction.confidence:.2%}")
