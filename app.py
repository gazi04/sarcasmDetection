from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from api.schemas import TrainingRequest, TrainingResponse, PredictionRequest, PredictionResponse, AnalysisResponse
from ai_core.training.pipeline import SarcasmDetectionPipeline

app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Sarcasm Detection API...")
    
    pipeline = SarcasmDetectionPipeline()
    app_state["pipeline"] = pipeline
    
    data = []
    try:
        with open('dataset.json', 'r', encoding='utf-8') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line:
                    item: dict = json.loads(stripped_line)
                    item.pop("article_link", None)
                    data.append(item)
    except FileNotFoundError:
        print("Warning: dataset.json not found. API will work but training needs data.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    
    if data:
        training_data = pipeline.prepare_data(data)
        app_state["training_data"] = training_data
        print(f"✅ Loaded {len(data)} samples")
    else:
        app_state["training_data"] = None
        print("⚠️ No data loaded")
    
    app_state["model_results"] = None
    
    print("✅ API startup completed!")
    yield
    print("👋 Shutting down API...")

app = FastAPI(
    title="Sarcasm Detection API",
    description="API for training and predicting sarcasm in headlines",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:5173", # <-- Add your frontend origin (default Vite port)
    "http://127.0.0.1:5173",  # <-- Add the IP equivalent
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"], # Allows all headers
)

@app.get("/")
async def root():
    return {
        "message": "Sarcasm Detection API",
        "endpoints": {
            "train": "POST /train - Train models with dataset",
            "predict": "POST /predict - Predict sarcasm in headline", 
            "analyze": "GET /analyze - Get dataset statistics"
        },
        "status": {
            "data_loaded": app_state.get("training_data") is not None,
            "models_trained": app_state.get("model_results") is not None
        }
    }

@app.post("/train", response_model=TrainingResponse)
async def train_models(request: TrainingRequest):
    try:
        pipeline = app_state["pipeline"]
        training_data = app_state["training_data"]
        
        if training_data is None:
            raise HTTPException(status_code=400, detail="No training data available")
        
        model_results = pipeline.train_models(training_data)
        app_state["model_results"] = model_results
        
        comparison = pipeline.get_training_comparison(model_results)
        
        return TrainingResponse(
            status="success",
            message="Models trained successfully",
            model_comparison=comparison["models"],
            best_model=comparison["best_model"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.post("/predict", response_model=PredictionResponse)
async def predict_headline(request: PredictionRequest):
    """Predict sarcasm using both models"""
    try:
        pipeline = app_state["pipeline"]
        model_results = app_state.get("model_results")
        
        if model_results is None:
            raise HTTPException(status_code=400, detail="No models trained yet. Please train models first.")
        
        predictions_data = pipeline.get_predictions(model_results, request.headline)
        
        return PredictionResponse(
            headline=predictions_data["headline"],
            predictions=predictions_data["predictions"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/analyze", response_model=AnalysisResponse)
async def analyze_dataset():
    """Get dataset statistics"""
    try:
        pipeline = app_state["pipeline"]
        training_data = app_state.get("training_data")
        
        if training_data is None:
            raise HTTPException(status_code=400, detail="No dataset available")
        
        pipeline.data_analysis(training_data)
        
        analysis_data = pipeline.get_analysis_data(training_data)
        
        return AnalysisResponse(**analysis_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/status")
async def get_status():
    """Get current API status"""
    return {
        "data_loaded": app_state.get("training_data") is not None,
        "models_trained": app_state.get("model_results") is not None,
        "data_samples": len(app_state["training_data"].headlines) if app_state.get("training_data") else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
