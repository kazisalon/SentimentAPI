from src.model.predictor import SentimentPredictor

def main() -> None:
    model = SentimentPredictor(model_name= "sentiment-v1", version = "2.0.0")

    model.load_model()

    sample_texts: list[str]= [
        "I love this product, it is amazing!",
        "Terrible experience, never again.",
        "It was okay, nothing special.",
    ]
    print("\n -- Testing Batch Predict (with Decorator)")
    predictions = model.predict(texts=sample_texts)
    print(f"Batch results: {predictions}\n")

    print("--Testing stream predict (with generator)")
    for result in model.stream_predict(texts=sample_texts):
        print(f"Streamed result: {result}")

if __name__== "__main__":
    main()