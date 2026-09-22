from helper import console, execute
import json
from pathlib import Path

with console.status("[bold cyan]Loading PyTorch...", spinner="dots"):
    import torch



def predict_reviews(texts, model_dir, batch_size=8):

    model_dir = Path(model_dir)

    # Load the class names saved during training.
    with open(model_dir / "labels.json","r",encoding="utf-8") as file:
         label_mapping = json.load(file)

    with console.status("[bold cyan]Loading transformers...", spinner="dots"):
         from transformers import (AutoTokenizer,AutoModelForSequenceClassification)
    # Load the fine-tuned model and its tokenizer.
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    model = AutoModelForSequenceClassification.from_pretrained(model_dir)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu" )

    model.to(device)
    model.eval()

    predictions = []

    # Process reviews in batches rather than individually.
    with torch.inference_mode():

        for start in range(0, len(texts), batch_size):

            batch = texts[start:start + batch_size]

            tokens = tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )

            tokens = {
                key: value.to(device)
                for key, value in tokens.items()
            }

            outputs = model(**tokens)

            class_ids = outputs.logits.argmax(
                dim=-1
            ).tolist()

            predictions.extend(
                label_mapping[str(class_id)]
                for class_id in class_ids
            )

    return predictions


def main():

    import pandas as pd

    df = pd.read_csv("samples_cleaned.csv")

    # Inspect the class distribution in our labeled dataset.
    print("\nActual price-range distribution:")
    print(df["price_range"].value_counts().sort_index())

    # Select examples from every available price category.
    samples = df.groupby(
        "price_range",
        group_keys=False
    ).head(3)

    predictions = predict_reviews(
        samples["text"].tolist(),
        "yelp_price_model"
    )

    print("\nActual vs. predicted price ranges:")

    for actual, predicted in zip(samples["price_range"], predictions):
        print(f"Actual: {actual} | Predicted: {predicted}")


if __name__ == "__main__":
    execute(main)