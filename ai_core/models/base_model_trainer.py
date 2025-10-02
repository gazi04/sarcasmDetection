from abc import ABC, abstractmethod
from typing import List
from sklearn.model_selection import train_test_split

from ai_core.data.models import ModelResult, TrainingData
from ai_core.config import ModelConfig

class BaseModelTrainer(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config
    
    @abstractmethod
    def train(self, data: TrainingData) -> ModelResult:
        pass
    
    def _split_data(self, headlines: List[str], labels: List[int]):
        return train_test_split(
            headlines, 
            labels, 
            test_size=self.config.test_size,
            random_state=self.config.random_state,
            stratify=labels
        )
