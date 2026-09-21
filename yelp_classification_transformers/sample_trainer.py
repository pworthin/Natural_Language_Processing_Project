
from helper import (console)

with console.status("[bold cyan]Loading transformers...", spinner="dots"):
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

with console.status("[bold cyan]Loading PyTorch...", spinner="dots"):
    import torch


with console.status("[bold cyan]Importing PyTorch dataset libary...", spinner="dots"):
    from torch.utils.data import Dataset




#Error handling is handled in the helper.py file

def tokenizer(frame):
    
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    tokenizer.save_pretrained(".\\yelp_price_model")

    print("Model and tokenizer saved to .\\yelp_price_model")
    tokens = tokenizer(
        frame["text"].tolist(),
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    labels = torch.tensor(frame["price_label"].tolist())
    return tokens, labels

    


class YelpDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            'input_ids': self.encodings['input_ids'][idx],
            'attention_mask': self.encodings['attention_mask'][idx],
            'labels': self.labels[idx]
        }


def ds_obj(tokens, labels):
    
    train_dataset = YelpDataset(tokens, labels)
    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=4
    )
    return model, train_dataset

    


def model_trainer(model, train_dataset):
    
    from transformers import TrainingArguments, Trainer
    if torch.cuda.is_available():
        model = model.to("cuda")
        print("Model sent to GPU")
    else:
        print("CUDA not available. Training on CPU")
    training_args = TrainingArguments(
        output_dir=".\\yelp_price_model",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        #evaluation_strategy="no",
        logging_steps=10,
        save_strategy="no",
        learning_rate=2e-5,
        weight_decay=0.01,
        seed=42
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset
    )

    trainer.train()
    model.save_pretrained(".\yelp_price_model")
    