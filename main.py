import json

from ai_core.utils.preproces import text_preprocessing
from ai_core.training.pipeline import SarcasmDetectionPipeline

data = []

try:
    with open('dataset.json', 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            
            if stripped_line:
                item:dict = json.loads(stripped_line)
                item.pop("article_link")
                processed_headline = text_preprocessing(item["headline"])
                data.append(item)
except FileNotFoundError:
    print("Error: The file 'dataset.json' was not found.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON from a line. Details: {e}")


pipeline = SarcasmDetectionPipeline()
training_data = pipeline.prepare_data(data)

print(f"Loaded {len(training_data.headlines)} headlines")
# pipeline.data_analysis(training_data)

model_results = pipeline.train_models(training_data)

test_headlines = [
    "Scientists discover that staring at screens all day is great for your health",
    "Breaking news: local man goes to work on Monday",
    "Israel 'tightens siege' of Gaza City as Hamas reviews Trump peace plan",
]

pipeline.run_predictions(model_results, test_headlines)
pipeline.print_summary(model_results)
