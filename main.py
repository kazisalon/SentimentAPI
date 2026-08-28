from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
from src.database.models import Base
from src.database.session import engine
# Import your ML Model
from src.model.predictor import SentimentPredictor
# Import your Pydantic schemas
from src.api.schemas import SentimentRequest, SentimentResponse, SentimentResult
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.database.models import PredictionLog

# 1. Initialize the FastAPI app
app = FastAPI(
    title="SentimentAPI",
    description="A production-grade ML serving API.",
    version="1.0.0"
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[DATABASE] Tables created/verified successfully.")
    
    yield  # This is where the app runs
    
    # SHUTDOWN: Clean up connections (optional but good practice)
    await engine.dispose()
    print("[DATABASE] Connections closed.")

# Update your app initialization to include the lifespan:
app = FastAPI(
    title="SentimentAPI",
    description="A production-grade ML serving API with DB logging.",
    version="1.0.0",
    lifespan=lifespan  # <-- Add this line
)

# 2. DEPENDENCY INJECTION: The "get_model" function
# FastAPI will call this function and inject the result into your endpoints.
def get_model() -> SentimentPredictor:
    """
    Dependency that provides the Singleton ML model instance.
    """
    # Because it's a Singleton, calling this multiple times just returns the same object
    model = SentimentPredictor(model_name="sentiment-v1", version="2.0.0")
    
    # Ensure it's loaded (in a real app, we'd do this in a startup event)
    if not model._is_loaded:
        model.load_model()
        
    return model

# 3. HEALTH CHECK ENDPOINT
@app.get("/health", tags=["System"])
async def health_check():
    """Standard endpoint for load balancers to check if the server is alive."""
    return {"status": "healthy", "service": "SentimentAPI"}

# 4. MAIN PREDICTION ENDPOINT
@app.post("/predict", response_model=SentimentResponse, tags=["ML"])
async def predict_sentiment(
    request: SentimentRequest, 
    model: SentimentPredictor = Depends(get_model),
    db: AsyncSession = Depends(get_db)  # <-- Inject the DB session!
):
    try:
        # 1. Get prediction from model
        raw_predictions = await model.predict(texts=request.texts)
        
        # 2. LOG TO DATABASE (We'll log the first text for this example)
        first_text = request.texts[0]
        first_score = raw_predictions[0]
        
        new_log = PredictionLog(
            model_name=model.model_name,
            input_text=first_text,
            prediction_scores=first_score
        )
        
        # Add to session and commit to the database
        db.add(new_log)
        await db.commit()
        await db.refresh(new_log)  # This populates the `id` and `created_at`
        
        # 3. Format and return response
        formatted_predictions = [SentimentResult(**pred) for pred in raw_predictions]
        
        return SentimentResponse(
            model_name=model.model_name,
            predictions=formatted_predictions
        )
    except Exception as e:
        await db.rollback()  # Rollback if something fails
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")

# 5. STREAMING ENDPOINT (Using your Generator from M1)
@app.post("/stream", tags=["ML"])
async def stream_sentiment(
    request: SentimentRequest,
    model: SentimentPredictor = Depends(get_model)
):
    """
    Streams predictions one by one. Great for massive batches.
    """
    import json
    
    async def generate_results():
        # Use the async generator we built in Milestone 1
        async for result in model.stream_predict(texts=request.texts):
            # FastAPI's StreamingResponse requires bytes or strings
            yield json.dumps(result) + "\n"

    return StreamingResponse(
        generate_results(), 
        media_type="application/x-ndjson" # Newline Delimited JSON
    )