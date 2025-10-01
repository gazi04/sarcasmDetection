import json

from model_training import main
from preproces import text_preprocessing
from utils import count_characters, count_words

data = []
words_per_headline:list[int] = []
chars_per_headline: list[int] = []
word_lengths: list[int] = []

try:
    with open('dataset.json', 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            
            if stripped_line:
                item:dict = json.loads(stripped_line)
                item.pop("article_link")
                processed_headline = text_preprocessing(item["headline"])

                words_per_headline.append(count_words(processed_headline))
                chars_per_headline.append(count_characters(processed_headline))
                
                # for word in item.get("headline").

                data.append(item)
                
except FileNotFoundError:
    print("Error: The file 'dataset.json' was not found.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON from a line. Details: {e}")


if __name__ == "__main__":
    print(f"Successfully loaded {len(data)} records.")
    
    model, vectorizer, accuracy = main(data)
    
