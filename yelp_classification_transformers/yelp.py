from helper import(
    console,
    progress,
    error_msg
)

console.print("Loading program. Please wait...\n")

import pandas as pd

import requests
from sklearn.preprocessing import LabelEncoder

#from transformers import pipeline, AutoTokenizer

with console.status("[bold cyan]Loading datasets...", spinner="dots"):
    from datasets import load_dataset, logging
with console.status("[bold cyan]Loading PyTorch", spinner="dots"):    
    from torch.utils.data import Dataset

#from sample_trainer import tokenizer, ds_obj, model_trainer


logging.set_verbosity_error() #This is to quiet all the console chattering when the dataset
                            #is being loaded
def data_prep():
    try:
        with progress(transient=True) as p: # transient keyword cleans up after it's done
            
            task = p.add_task("Loading Yelp dataset...", start=True)
            #p.start_task(task)

            ds = load_dataset("Yelp/yelp_review_full", cache_dir="hf_cache")
            df = ds["train"].to_pandas()

        print("[✓] Done loading dataset.")

        classification(df)
        return df
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error[/red]: [orange1]{e}[/orange1]")
        exit(1)
    except Exception as e:
        error_msg(e)

def classification(frame):
    try:

        new_df = pd.read_csv('samples_cleaned.csv')

        # Encode price_range labels to integers
        label_encoder = LabelEncoder()
        new_df["price_label"] = label_encoder.fit_transform(new_df["price_range"])
        label_classes = list(label_encoder.classes_)
        print("Price range classes:", label_classes)
        print(new_df)
    except Exception as e:
        error_msg(e)


def main():
    try:
        frame = data_prep()
        classification(frame)

        print('\nTask completed.')
    except Exception as e:
        error_msg(e)

if __name__ == "__main__":
    main()