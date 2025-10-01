import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from preproces import text_preprocessing


def prepare_data(data):
    headlines = []
    labels = []

    for item in data:
        processed_text = text_preprocessing(item["headline"])
        headlines.append(processed_text)
        labels.append(item["is_sarcastic"])

    return headlines, labels


def train_logistic_regression_tfidf(headlines, labels):

    X_train, X_test, y_train, y_test = train_test_split(
        headlines, labels, test_size=0.2, random_state=42, stratify=labels
    )

    tfidf_vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        stop_words="english",
        min_df=2,
        max_df=0.8,
    )

    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        class_weight="balanced",
    )

    model.fit(X_train_tfidf, y_train)

    return model, tfidf_vectorizer, X_test_tfidf, y_test, X_train, X_test


def evaluate_model(model, X_test_tfidf, y_test):

    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)

    print("🔍 Model Evaluation Results:")
    print(f"📊 Accuracy: {accuracy:.4f}")
    print("\n📈 Detailed Classification Report:")
    print(
        classification_report(
            y_test, y_pred, target_names=["Not Sarcastic", "Sarcastic"]
        )
    )

    return y_pred, accuracy


def plot_confusion_matrix(y_test, y_pred):
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Not Sarcastic", "Sarcastic"],
        yticklabels=["Not Sarcastic", "Sarcastic"],
    )
    plt.title("Confusion Matrix - Sarcasm Detection")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()

    plt.savefig("confusion_matrix.png", dpi=300, bbox_inches="tight")
    print("Confusion matrix saved as 'confusion_matrix.png'")
    plt.close()


def predict_sarcasm(model, vectorizer, new_text):
    processed_text = text_preprocessing(new_text)
    features = vectorizer.transform([processed_text])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    result = "Sarcastic" if prediction == 1 else "Not Sarcastic"
    confidence = probability[1] if prediction == 1 else probability[0]

    print(f"Headline: '{new_text}'")
    print(f"Prediction: {result}")
    print(f"Confidence: {confidence:.2%}")

    return prediction, confidence


def train_naive_bayes(headlines, labels):
    X_train, X_test, y_train, y_test = train_test_split(
        headlines, labels, test_size=0.2, random_state=42, stratify=labels
    )

    count_vecotrizer = CountVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        stop_words="english",
        min_df=2,
        max_df=0.8,
    )

    X_train_multinomial = count_vecotrizer.fit_transform(X_train)
    X_test_multinomial = count_vecotrizer.transform(X_test)

    model = MultinomialNB()

    model.fit(X_train_multinomial, y_train)

    return model, count_vecotrizer, X_test_multinomial, y_test, X_train, X_test

def compare_models(lr_accuracy, nb_accuracy, lr_predictions, nb_predictions, y_test, model_names=None):
    """
    Simple model comparison showing which performs better
    """
    if model_names is None:
        model_names = ['Logistic Regression', 'Naive Bayes']
    
    print("=" * 50)
    print("MODEL COMPARISON")
    print("=" * 50)
    
    print(f"{model_names[0]} Accuracy: {lr_accuracy:.2%}")
    print(f"{model_names[1]} Accuracy: {nb_accuracy:.2%}")
    print()
    
    if lr_accuracy > nb_accuracy:
        winner = model_names[0]
        difference = lr_accuracy - nb_accuracy
        print(f"WINNER: {winner} (by {difference:.2%})")
    elif nb_accuracy > lr_accuracy:
        winner = model_names[1]
        difference = nb_accuracy - lr_accuracy
        print(f"WINNER: {winner} (by {difference:.2%})")
    else:
        print("MODELS TIED - Same accuracy!")
    
    print()
    print("=" * 50)
    
    best_model = model_names[0] if lr_accuracy >= nb_accuracy else model_names[1]
    best_accuracy = max(lr_accuracy, nb_accuracy)
    
    return best_model, best_accuracy


def main(data):
    print("Starting Model Training...")
    
    headlines, labels = prepare_data(data)
    
    lr_model, lr_vectorizer, X_test_tfidf, y_test, X_train, X_test = train_logistic_regression_tfidf(headlines, labels)
    lr_predictions, lr_accuracy = evaluate_model(lr_model, X_test_tfidf, y_test)
    
    nb_model, nb_vectorizer, X_test_counts, y_test, X_train, X_test = train_naive_bayes(headlines, labels)
    nb_predictions, nb_accuracy = evaluate_model(nb_model, X_test_counts, y_test)
    
    best_model, best_accuracy = compare_models(
        lr_accuracy, nb_accuracy, 
        lr_predictions, nb_predictions, 
        y_test
    )
    
    print(f"\n RECOMMENDATION: Use {best_model} with {best_accuracy:.2%} accuracy")
    
    return best_model, lr_model if best_model == 'Logistic Regression' else nb_model, best_accuracy
