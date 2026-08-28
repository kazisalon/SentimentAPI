from src.model.predictor import SentimentPredictor

def main() -> None:
    model = SentimentPredictor(model_name= "sentiment-v1", version = "2.0.0")

    model.load_model()

    sample_texts: list[str]= [
        "I love this product, it is amazing!",
        "Terrible experience, never again.",
        "It was okay, nothing special.",
    ]

    predictions = model.predict(texts=sample_texts)

    for text, pred in zip(sample_texts, predictions):
        print(f"Text: '{text}'")
        print(f"Scores: {pred}")
        print("--")

    broken_model = SentimentPredictor(model_name="broken")
    try:
        broken_model.predict(texts=["test"])
    except RuntimeError as e:
        print(f"Caught expected error: {e}")

if __name__== "__main__":
    main()