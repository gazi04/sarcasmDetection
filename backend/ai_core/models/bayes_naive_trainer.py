from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from ai_core.data.models import ModelResult, TrainingData
from ai_core.models.base_model_trainer import BaseModelTrainer

class NaiveBayesTrainer(BaseModelTrainer):
    def train(self, data: TrainingData) -> ModelResult:
        X_train, X_test, y_train, y_test = self._split_data(data.headlines, data.labels)
        
        vectorizer = CountVectorizer(
            max_features=self.config.max_features,
            ngram_range=self.config.ngram_range,
            stop_words="english",
            min_df=self.config.min_df,
            max_df=self.config.max_df,
        )
        
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)
        
        model = MultinomialNB()
        model.fit(X_train_vec, y_train)
        predictions = model.predict(X_test_vec)
        
        return ModelResult(
            model=model,
            vectorizer=vectorizer,
            X_test=X_test_vec,
            y_test=y_test,
            predictions=predictions,
            accuracy=0.0,
            model_name="Naive Bayes"
        )
