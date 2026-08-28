import time
import asyncio
from typing import List, Dict, Any
from src.utils.timing import log_inference_time

class SentimentPredictor:
    """ A mock sentiment analysis model, In later phases this will wrap a real ml
    ML model ( e.g, Hugging face) for now, it stimulates one. """

    LABELS: List[str] = ["positive", "negative", "neutral"]

    # 1 class variable to hold the single instance

    _instance: 'SentimentPredictor | None'= None
    #2 Override __new__ to control object creation 
    def __new__(cls, *args: Any, **kwargs: Any) -> 'SentimentPredictor':
            if cls._instance is None:
                    print("[SINGLETON] Creating the one and only model instance")
                    cls._instance = super(SentimentPredictor, cls).__new__(cls)
            else:
                    print("[SINGLETON] Reusing Existing model instance")
            return cls._instance
            
    def __init__(self, model_name: str, version:str = "1.0.0") -> None:
                 if hasattr(self, '_is_loaded'):
                         return
                         
                 self.model_name: str = model_name
                 self.version:str = version
                 self._is_loaded: bool = False


    def load_model(self) -> None:
            print(f"Loading model. '{self.model_name}'v{self.version}...")
            time.sleep(1)
            self._is_loaded = True
            print("Model Loaded Successfully. ")
    @log_inference_time        
    async def predict(self, texts:List[str]) -> List[Dict[str, float]]:
            if not self._is_loaded:
                    raise RuntimeError("Model not loaded. Call load_model() first.")
            await asyncio.sleep(0.5)

            results: List[Dict[str, float]] = []
            for text in texts:
                    score = len(text) / 100.0
                    result: Dict[str, float] = {
                            "positive" : min(score, 1.0), 
                            "negative" : max(1.0 - score, 0.0),
                            "neutral": 0.1, 

                    }
                    results.append(result)

            return results


    async def stream_predict(self, texts: List[str]):
            if not self._is_loaded:
                    raise RuntimeError("Model not Loaded. Call load_model() first.")

            for text in texts:
                    await asyncio.sleep(0.2)
                    score = len(text)/100.0
                    yield {
                            "text": text,
                            "positive": min(score, 1.0),
                            "negative": max(1.0 - score, 0.0),
                            "neutral": 0.1,
                    }