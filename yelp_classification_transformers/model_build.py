from helper import execute
import pandas as pd
from sample_trainer import tokenizer, ds_obj, model_trainer
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv("samples_cleaned.csv")

def main():

    label_encoder = LabelEncoder()
    df["price_label"] = label_encoder.fit_transform(df["price_range"])

    tokens, labels = tokenizer(df)
    model, train_dataset = ds_obj(tokens, labels)
    model_trainer(model, train_dataset)

  
if __name__ == '__main__':
    execute(main)