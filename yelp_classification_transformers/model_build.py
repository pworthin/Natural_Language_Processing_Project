import sys

import signal
import traceback
import os

import pandas as pd
from sample_trainer import tokenizer, ds_obj, model_trainer
from sklearn.preprocessing import LabelEncoder
##################### Setup Functions #####################

#print("\n\nLoading Program. Please wait...")

# This sets the system colors #
GREEN = '\u001b[92m'
RED = '\u001b[91m'
ORANGE = '\u001b[38;5;208m'
RESET = '\u001b[0m'


def error_msg(e):
    print(f"{RED}Error{RESET}: {ORANGE}{e}{RESET}")
    traceback.print_exc()
    sys.exit(1)


# Terminates the program on Ctrl+C
def sigint_handler(signum, frame):
    print("\nTerminating program...\n")
    sys.exit(0)


signal.signal(signal.SIGINT, sigint_handler)


def silence():  # This is for when the console is complaining about something petty
    sys._stderr = sys.stderr  # Backup just once
    sys.stderr = open(os.devnull, 'w')


def restore_sanity():  # This restores error output after being silenced
    if hasattr(sys, '_stderr'):
        sys.stderr = sys._stderr  # Restore
        del sys._stderr


#########################################################

df = pd.read_csv("samples_cleaned.csv")

def main():
    try:
        label_encoder = LabelEncoder()
        df["price_label"] = label_encoder.fit_transform(df["price_range"])

        tokens, labels = tokenizer(df)
        model, train_dataset = ds_obj(tokens, labels)
        model_trainer(model, train_dataset)



    except Exception as e:
        error_msg(e)

if __name__ == '__main__':
    main()