from helper import(
    console,
    progress,
    silencer,
    execute,
    terminate_signal
   
)
terminate_signal()
console.print("Loading program. Please wait...\n")

import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import LabelEncoder

with console.status("[bold cyan]Loading datasets...", spinner="dots"):
    from datasets import load_dataset


silencer("ds_logger", "hf")#This is to quiet all the console chattering when the dataset
                              #is being loaded


def data_prep():
    try:
        with progress(transient=True) as p: # transient keyword cleans up after it's done
            
            p.add_task("Loading Yelp dataset...", start=True)
            #p.start_task(task)

            ds = load_dataset("Yelp/yelp_review_full", cache_dir="hf_cache")
            df = ds["train"].to_pandas()

        print("[✓] Done loading dataset.")

        #classification(df)
        return df
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error[/red]: [orange1]{e}[/orange1]")
        exit(1)

def prepare_analysis_data(frame):
    """
    Prepare the Yelp dataframe for the original project analysis.

    Sentiment is derived from the original Yelp star-rating label.
    Cuisine and price range are synthetic categories for EDA.
    They are not verified restaurant attributes.
    """

    df = frame.copy()

    # Original Yelp labels: 0-4 represent 1-5 stars.
    sentiment_map = {
        0: "negative",
        1: "negative",
        2: "neutral",
        3: "positive",
        4: "positive",
    }

    df["sentiment"] = df["label"].map(sentiment_map)

    # Synthetic categories used for the coursework analysis.
    cuisines = [
        "American",
        "Mexican",
        "Chinese",
        "Italian",
        "Indian",
    ]

    price_ranges = [
        "$",
        "$$",
        "$$$",
        "$$$$",
    ]

    # Fixed seed makes the synthetic assignments reproducible.
    rng = np.random.default_rng(42)

    df["cuisine"] = rng.choice(
        cuisines,
        size=len(df)
    )

    df["price_range"] = rng.choice(
        price_ranges,
        size=len(df)
    )

    return df

def classification(frame):
    

    new_df = pd.read_csv('samples_cleaned.csv')

    # Encode price_range labels to integers
    label_encoder = LabelEncoder()
    new_df["price_label"] = label_encoder.fit_transform(new_df["price_range"])
    label_classes = list(label_encoder.classes_)
    print("Price range classes:", label_classes)
    print(new_df)
    


def main():

    frame = data_prep()
    frame = prepare_analysis_data(frame)
    print(f"\nPrepared {len(frame):,} reviews.")

    return frame

    

if __name__ == "__main__":
    execute(main)