"""
Data structures used throughout the pipeline.
- TrainingData: clean texts and labels prepared for modeling
- ModelResult: trained estimator, vectorizer, test split and metrics holder
- PredictionResult: single-sample prediction output with label and confidence
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import pandas as pd
from sklearn.base import BaseEstimator

@dataclass
class TrainingData:
    headlines: List[str]
    labels: List[int]
    
    def get_class_distribution(self) -> Dict[int, int]:
        return pd.Series(self.labels).value_counts().to_dict()

@dataclass
class ModelResult:
    model: BaseEstimator
    vectorizer: Any
    X_test: Any
    y_test: List[int]
    predictions: List[int]
    accuracy: float
    model_name: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "accuracy": self.accuracy,
            "test_set_size": len(self.y_test)
        }

@dataclass
class PredictionResult:
    text: str
    prediction: int
    confidence: float
    is_sarcastic: bool
    
    @property
    def prediction_label(self) -> str:
        return "Sarcastic" if self.is_sarcastic else "Not Sarcastic"
