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
    classification(frame)

    print('\nTask completed.')

    

if __name__ == "__main__":
    execute(main)