import sys
import signal
import traceback
import os
from rich.console import Console

from googletrans import Translator, LANGUAGES
from requests.exceptions import RequestException

##################### Setup Functions #####################

print("\n\nLoading Program. Please wait...")

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


def shutup():  # This is for when the console is complaining about something stupid
    sys._stderr = sys.stderr  # Backup just once
    sys.stderr = open(os.devnull, 'w')


def restore_sanity():  # This restores error output after being silenced
    if hasattr(sys, '_stderr'):
        sys.stderr = sys._stderr  # Restore
        del sys._stderr


#########################################################


disp_console = Console(width=100)


class PocketTranslator:
    def __init__(self, text, src, src_fn, dest, dest_fn):
        self.text = text
        self.src = src if src else 'auto'
        self.src_fn = src_fn
        self.dest = dest
        self.dest_fn = dest_fn

    def basic_translate(self):
        try:

            print("Translating text...")
            while True:
                if not len(self.text) < 1000:
                    self.text = disp_console.input("That phase is too long. Please keep it under 1000 characters!\n>>")
                    continue
                trans = Translator()

                display = trans.translate(text=self.text, src=self.src, dest=self.dest)

                return print(
                    f"\n{self.src_fn.capitalize()} -> {self.text}\n{self.dest_fn.capitalize()} -> {display.text}")


        except RequestException:
            print("Error: Google Translate servers are unreachable at this time. Please try again later.")
            exit(1)
        except Exception as e:
            error_msg(e)


#I'll get to this function later.....
def batch_translation(texts, src='en', dest='fr'):
    try:
        print("Translating text batch. Please wait...")
        if not isinstance(texts, list):
            raise TypeError("Expected a list of strings")

        trans = Translator()
        results = []

        for i in range(0, len(texts)):
            #This is important! A separate try/except must be used for the for-loop
            #If translation fails with any sentence, the entire program will terminate
            # if only the outer for-loop is implemented!
            try:
                translated_sent = trans.translate(texts[i], dest=dest, src=src)

                result = {
                    'original': texts[i],
                    'translated': translated_sent.text,
                    'src': src,
                    'dest': dest

                }
                results.append(result)
            except Exception as e:
                print(f"Error translating '{texts[i]}': {e} ")

        return results

    except Exception as e:
        error_msg(e)


def langcheck(languages):
    try:

        while True:

            src = languages[0]
            mark = languages[1]  #This is the '>' delimiter
            dest = languages[2]
            '''
            for i in languages:
                if not languages[i].isalpha() and languages[i] != languages[1]: # This is to prevent the delimiter '>'
                    languages = input("Invalid input.\n>> ")                    #from being caught as non alpahetical.
            if not src or not dest or mark != ">":
                languages = disp_console.input(
                    "Please enter all fields in the following format: (e.g \"English > German\") If you do"
                    " not know the name of the language you are trying to translate, type \"Unknown\". You may "
                    "also translate to multiple different languages (\"English > German, Spanish, French\")\n>>").lower().split(
                    ',')
                continue
                
                '''
            if len(languages) > 3:
                values = multilang(languages)
                return values

            if src == "unknown":
                src = None
            lang_lookup = {name.lower(): code for code, name in LANGUAGES.items()}

            src_code = lang_lookup.get(src)
            dest_code = lang_lookup.get(dest)

            src_full_name = LANGUAGES.get(src_code)
            dest_full_name = LANGUAGES.get(dest_code)

            if src_code and dest_code:

                return src_code, src_full_name, dest_code, dest_full_name
            else:
                retry = disp_console.input(
                    "I am sorry, I could not find that language. Please check the spelling and try again. Press Ctrl+C to end.\n>>").lower().split(
                    ',')
                langcheck(retry)

    except Exception as e:
        error_msg(e)


def multilang(languages):
    try:
        lang_array = []
        destcodes = []
        destfullnames = []
        for i in languages:
            lang_array.append(i)

        lang_lookup = {name.lower(): code for code, name in LANGUAGES.items()}
        src_code = lang_lookup.get(lang_array[0])
        src_full_name = LANGUAGES.get(src_code)

        for j in lang_array[2:]:
            code =lang_lookup.get(j.strip().lower())
            name = LANGUAGES.get(code)

            destcodes.append(code)
            destfullnames.append(name)

            return src_code, src_full_name, destcodes, destfullnames
    except Exception as e:
        error_msg(e)


def formatcheck(user_input):
    try:
        if '>' not in user_input:
            raise ValueError("Missing '>' delimiter. Use format like 'English > German, French'")

        parts = user_input.split('>')
        if len(parts) != 2:
            raise ValueError("Too many or too few '>' delimiters.")

        src = parts[0].strip().lower()
        dest_part = parts[1].strip().lower()
        dest_langs = [d.strip() for d in dest_part.split(',') if d.strip()]

        # Validate all parts
        if not src.replace(" ", "").isalpha():
            raise ValueError("Source language must contain only letters.")

        for lang in dest_langs:
            if not lang.replace(" ", "").isalpha():
                raise ValueError(f"Destination language '{lang}' is not valid.")

        return src, dest_langs
    except Exception as e:
        error_msg(e)

def main():
    try:

        languages = disp_console.input(
            "Please enter a language to translate from and a language to translate to (e.g. \"English > German \"). If you do not"
            " know the language, type \"Unknown > (Your language)\" and the system will auto-detect\n>>").lower().split(
            ',')

        sc, sfn, dc, dfn = langcheck(languages)  #Souce code, source full name, dest code, dest full name


        phrase = disp_console.input("Enter a phrase to translate:\n>> ")
        if type(dc) is list:
            for i in range(dc):
                my_translator = PocketTranslator(phrase, sc, sfn, dc[i], dfn[i])
                my_translator.basic_translate()
        else:
            my_translator = PocketTranslator(phrase, sc, sfn, dc, dfn)

            my_translator.basic_translate()

        '''
        sentences = ["The sun dipped below the horizon, casting a warm glow across the sky.",
                     "She eagerly opened the gift, revealing a beautiful necklace.",
                     "The children played happily in the park on a sunny afternoon.",
                     "He studied diligently for his upcoming exam.",
                     "The aroma of freshly baked bread filled the kitchen.",
                     "They decided to take a spontaneous road trip last weekend.",
                     "The mountain stream sparkled under the midday sun.",
                     "She whispered her secrets into the night sky.",
                     "The old bookstore was a treasure trove for bibliophiles.",
                     "A gentle breeze rustled the leaves of the ancient oak tree."]

        trans_list = batch_translation(sentences)
        print('*' * 125)
        for i in trans_list:
            print(f"\nOriginal: {i['original']}\nTranslated: {i['translated']}")

        '''

    except Exception as e:
        error_msg(e)


if __name__ == "__main__":
    main()
