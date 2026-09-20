import nltk
import sys
import signal
import traceback



from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



#### This kills the program if it enters an infinite loop ###

def sigint_handler(signum, frame):
    print("\nTerminating program...\n")
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)


def error_msg(e):
    #This is to generate an error message
    print(f"{RED}Error:{RESET} {e}\n\n")
    traceback.print_exc()
    sys.exit(1)
#############################################################

#This sets the system colors#

GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

#tqdm.pandas(leave=False) #This enables the progress bar for Pandas library

def error_msg(e):
    #This is to generate an error message
    print(f"{RED}Error:{RESET} {e}\n\n")
    traceback.print_exc()
    sys.exit(1)
##############################################################


def main():

    print('Program loading. Please wait...')
    try:
        nltk.download('reuters', quiet=True)
        documents = reuters.fileids()
        corpus = [reuters.raw(doc_id) for doc_id in documents]


    except Exception as e:
        error_msg(e)