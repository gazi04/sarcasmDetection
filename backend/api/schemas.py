from pydantic import BaseModel
from typing import List, Dict, Any

class ModelComparison(BaseModel):
    name: str
    type: str
    accuracy: float
    test_set_size: int

class TrainingResponse(BaseModel):
    status: str
    message: str
    model_comparison: List[ModelComparison]
    best_model: str

class PredictionResult(BaseModel):
    model_name: str
    model_type: str
    prediction: str
    is_sarcastic: bool
    confidence: float

class PredictionResponse(BaseModel):
    headline: str
    predictions: List[PredictionResult]

class BasicStatistics(BaseModel):
    total_samples: int
    sarcastic_samples: int
    non_sarcastic_samples: int
    sarcastic_percentage: float
    non_sarcastic_percentage: float
    class_distribution: Dict[str, int]

class WordFrequency(BaseModel):
    word: str
    frequency: int

class TextLengthStats(BaseModel):
    average_words: Dict[str, float]
    length_range: Dict[str, int]

class AnalysisResponse(BaseModel):
    basic_statistics: BasicStatistics
    word_frequencies: Dict[str, List[WordFrequency]]
    text_length_stats: TextLengthStats

class TrainingRequest(BaseModel):
    # If you want to allow custom training data via API
    data: List[Dict[str, Any]]

class PredictionRequest(BaseModel):
    headline: str
