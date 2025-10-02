from dataclasses import dataclass

@dataclass
class ModelConfig:
    test_size: float = 0.2
    random_state: int = 42
    max_features: int = 5000
    ngram_range: tuple = (1, 3)
    min_df: int = 2
    max_df: float = 0.8

@dataclass
class LogisticRegressionConfig(ModelConfig):
    max_iter: int = 1000
    class_weight: str = "balanced"

@dataclass
class PathConfig:
    confusion_matrix_path: str = "confusion_matrix"
    model_save_path: str = "results/"

class Constants:
    CLASS_NAMES = ["Not Sarcastic", "Sarcastic"]
    POSITIVE_CLASS = 1
    NEGATIVE_CLASS = 0
