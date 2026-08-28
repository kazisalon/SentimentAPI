import time
from typing import List, Dict
from src.utils.timing import log_inference_time

class SentimentPredictor:
    """ A mock sentiment analysis model, In later phases this will wrap a real ml
    ML model ( e.g, Hugging face) for now, it stimulates one. """

    LABELS: List[str] = ["positive", "negative", "neutral"]

    def __init__(self, model_name: str, version:str = "1.0.0") -> None:
                 self.model_name: str = model_name
                 self.version:str = version
                 self._is_loaded: bool = False


    def load_model(self) -> None:
            print(f"Loading model. '{self.model_name}'v{self.version}...")
            time.sleep(1)
            self._is_loaded = True
            print("Model Loaded Successfully. ")
    @log_inference_time        
    def predict(self, texts:List[str]) -> List[Dict[str, float]]:
            if not self._is_loaded:
                    raise RuntimeError("Model not loaded. Call load_model() first.")

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


    def stream_predict(self, texts: List[str]):
            if not self._is_loaded:
                    raise RuntimeError("Model not Loaded. Call load_model() first.")

            for text in texts:
                    time.sleep(0.2)
                    score = len(text)/100.0
                    yield {
                            "text": text,
                            "positive": min(score, 1.0),
                            "negative": max(1.0 - score, 0.0),
                            "neutral": 0.1,
                    }