# 🎭 Sarcasm Detector

This project provides AI models that are trained with news headlines to identify them if they're sarcastic or not. The dataset used in this project is free and you can get it in this link down below:
	https://www.kaggle.com/datasets/rmisra/news-headlines-dataset-for-sarcasm-detection/data

- **The Problem:** In the rapid-fire world of online news, sarcastic headlines are often mistaken for literal facts, fueling confusion, outrage, and the spread of fake news. This erodes trust in media and creates a polarized information landscape.
- **Our Solution:** The Sarcasm Detector is a specialized AI tool that analyzes the language, context, and patterns in news headlines to instantly identify sarcasm with high accuracy.
- **The Value:** For **readers**, it’s a simple website where you can put the headline and that for preventing misinterpretation.

# ✨ Features

1. Two predictive models, that includes the Logistic Regression and Naive Bayes
2. FastAPI endpoints for the backend
3. Simple dashboard with Vue.js


#  Quick Start / Installation

## Prerequisites

- **Python**: 3.13+
- One of:
  - **uv** (recommended) — fast Python package manager
  - or **pip + venv**
- **Node.js**: 20.x or 22.x, and **npm**

Optional (first run will auto-download): internet access for **NLTK** data

## 1. 🐍 Backend (FastAPI)

All backend code and config live in `backend/`.

###  📦 Install dependencies

Using uv (recommended):

```
cd backend
uv sync
```

Using pip + venv:

```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

###  📊 Dataset

- A sample `dataset.json` is already in `backend/`.
- If you replace it, download the Kaggle dataset and place the JSON Lines file as `backend/dataset.json` (one JSON object per line). The app removes the `article_link` field automatically.

###  Run the API server

From `backend/`:

Using uv:

```
uv run uvicorn app:app --reload
```

Or with an active venv:

```
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

- Swagger UI: `http://localhost:8000/docs`
- CORS is enabled for `http://localhost:5173` (frontend dev server)

### (Optional) CLI training run

From `backend/` you can run the end‑to‑end training and demo predictions in the terminal:

Using uv:

```
uv run python main.py
```

Or with an active venv:

```
python main.py
```

This will load the dataset, analyze it, train both models, run sample predictions, and print a brief summary. Confusion matrices are saved in `backend/results/`.

## 2) Frontend (Vue 3 + Vite)

With the backend running on `http://localhost:8000`:

```
cd front
npm ci # 📦 install dependecies
npm run dev # 🌐 run the website
```

Open the URL printed by Vite (typically `http://localhost:5173/`). The app is preconfigured to call the API at `http://localhost:8000`.
# 📖 Usage
There are different ways on how to actually use the project:
## 1. Terminal approach 

For this method there is a sample code in the main.py so all you need to do is run(execute) the code and it will load the data, show some statistics about the raw dataset, train the model, also you can give it a headline to make predictions and as last it gives you a summary of the model result.  

Put your headlines in the **test_headlines** list as shown below:
```
print(f"Loaded {len(training_data.headlines)} headlines")
pipeline.data_analysis(training_data)

model_results = pipeline.train_models(training_data)

# PUT HERE YOUR HEADLINES
test_headlines = [
    "Scientists discover that staring at screens all day is great for your health",
    "Breaking news: local man goes to work on Monday",
    "Israel 'tightens siege' of Gaza City as Hamas reviews Trump peace plan",
]

pipeline.run_predictions(model_results, test_headlines)
pipeline.print_summary(model_results)
```

## 2. FastAPI with Swager UI

In this approach you could only run the commands in the terminal
```
	uv run uvicorn app:app --reload # If you use uv as package manager
	# Or 
	uvicorn app:app --reload
```

that will run the web server. A good feature that FastAPI offers is the interactive API documentation and exploration web user interface with Swagger UI by entering /docs into your URL you will be shown this view like in the image below, the URL should look like this ==localhost:8000/docs==. 

![[docs/images/swaggerUI.png]]


## 3.  Use the front end project to consume the API's
In this method first in the /backend directory run the previous command to run the web server and then in /front directory run the Vue project with the command:
```
npm run dev
```

As result it will give you the URL, in most cases it would be **localhost:5173/**, and by entering the URL in your preferred browser it will show you a simple to use dashboard.

## 📚 Documentation

For more details, see our [docs folder](docs/Table%20of%20Content.md).




