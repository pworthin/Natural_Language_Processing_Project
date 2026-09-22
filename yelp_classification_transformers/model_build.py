"""
This is an optional file to train separate transformer model
"""

import pandas as pd
import json
from pathlib import Path
from sample_trainer import tokenizer, ds_obj, model_trainer
from sklearn.preprocessing import LabelEncoder
from helper import execute, silencer

silencer("hf")
df = pd.read_csv("samples_cleaned.csv")

def save_label_mapping(encoder, output_dir):

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    mapping = {str(index): str(label)for index, label in enumerate(encoder.classes_)}
    with open(Path(output_dir) / "labels.json","w",encoding="utf-8") as file:
        json.dump(mapping, file, indent=4)
    print(f"Label mapping saved to {output_dir}/labels.json")


def main():

    # ---------- Price-range classifier ----------

    price_encoder = LabelEncoder()
    df["price_label"] = price_encoder.fit_transform(
        df["price_range"]
    )

    print("\nPrice range classes:", list(price_encoder.classes_))
    tokens, labels = tokenizer( df, "yelp_price_model","price_label")
    model, train_dataset = ds_obj(tokens,labels, len(price_encoder.classes_))
    model_trainer(model,train_dataset, "yelp_price_model" )

    # ---------- Cuisine classifier ----------

    cuisine_encoder = LabelEncoder()

    df["cuisine_label"] = cuisine_encoder.fit_transform(
        df["cuisine"]
    )

    print("\nCuisine classes:", list(cuisine_encoder.classes_))
    tokens, labels = tokenizer(df,"yelp_cuisine_model", "cuisine_label")
    model, train_dataset = ds_obj(tokens,labels,len(cuisine_encoder.classes_))
    model_trainer(model,train_dataset,"yelp_price_model")
    save_label_mapping(price_encoder, "yelp_price_model")
    model_trainer(model,train_dataset,"yelp_cuisine_model")
    save_label_mapping(cuisine_encoder,"yelp_cuisine_model")
    
if __name__ == "__main__":
    execute(main)