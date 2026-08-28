from src.model.predictor import SentimentPredictor
import asyncio

async def main() -> None:
    print("---testing singleton pattern")
    model1 = SentimentPredictor(model_name= "sentiment-v1", version = "2.0.0")
    model2 = SentimentPredictor(model_name= "sentiment-v2", version = "3.0.0")

    print(f"are they the same object ? {model1 is model2 }")
    model1.load_model()

    sample_texts: list[str]= [
        "I love this product, it is amazing!",
        "Terrible experience, never again.",
        
    ]
    print("\n -- Testing Async Batch Predict (with Decorator)")
    predictions = await model1.predict(texts=sample_texts)
    print(f"Batch results: {predictions}\n")

    print("--Testing async stream predict (with generator)")
    async for result in model1.stream_predict(texts=sample_texts):
        print(f"Streamed result: {result}")

if __name__== "__main__":
    asyncio.run(main())