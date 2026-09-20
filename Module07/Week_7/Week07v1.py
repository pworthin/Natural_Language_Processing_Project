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


# sc : source language code (e.g. en, de, es)
# sfn : source full name (e.g English, German, Spanish)
# dc : Destination language code
# dfn : Destination full name
class PocketTranslator:
    def __init__(self, text, src, src_fn, dest, dest_fn):
        self.text = text
        self.src = src
        self.src_fn = src_fn
        self.dest = dest
        self.dest_fn = dest_fn

    def basic_translate(self):
        try:

            #print("Translating text...")
            while True:
                if len(self.text) > 1000:
                    self.text = disp_console.input("That phase is too long. Please keep it under 1000 characters!\n>>")
                    continue
                trans = Translator()
                if self.src =='auto': #This is the autolook
                    self.src, self.src_fn = autolookup(self.text)

                display = trans.translate(text=self.text, src=self.src, dest=self.dest)

                return print(
                    f"\n{self.src_fn.capitalize()} -> {self.text}\n{self.dest_fn.capitalize()} -> {display.text}")


        except RequestException:
            print("Error: Google Translate servers are unreachable at this time. Please try again later.")
            exit(1)
        except Exception as e:
            error_msg(e)


    def batch_translation(self, text):
        try:
            #print("Translating text batch. Please wait...")
            if not isinstance(self.text, list):
                raise TypeError("Expected a list of strings")

            trans = Translator()
            results = []

            for i in range(0, len(text)):
                #This is important! A separate try/except must be used for the for-loop
                #If translation fails with any sentence, the entire program will terminate
                # if only the outer for-loop is implemented!
                try:
                    if self.src == 'auto':
                        self.src, self.src_fn = autolookup(text[i])
                    if len(text[i]) > 1000:
                        text = disp_console.input(
                            "This phase is too long. Please keep it under 1000 characters! Moving to the next...\n>>")

                        continue
                    translated_sent = trans.translate(text[i], dest=self.dest, src=self.src)

                    result = {
                        'original': text[i],
                        'translated': translated_sent.text,
                        'src': self.src,
                        'dest': self.dest

                    }
                    results.append(result)
                except Exception as e:
                    print(f"Error translating '{text[i]}': {e} ")

            return results

        except Exception as e:
            error_msg(e)


def formatcheck(user_input):
    try:
        # Check for presence of delimiter. This is to keep the line of programming from confusing itself
        #It needs to know that everything after the delimiter is the dest language.
        if '>' not in user_input:
            raise ValueError("Missing '>' delimiter. Use format like 'English > German, French'")

        # Split into source and destination parts
        parts = user_input.split('>')
        if len(parts) != 2:
            raise ValueError("Too many or too few '>' delimiters.")

        # Here is where we strip awy the whitespaces and the commas entered by the user and isolate
        # the parts
        src = parts[0].strip().lower()
        dest_part = parts[1].strip().lower()
        dest_langs = [d.strip() for d in dest_part.split(',') if d.strip()]  # ['german', 'french']

        # Check if input is alphabetic
        if not src.replace(" ", "").isalpha():
            raise ValueError("Source language must contain only letters.")

        for lang in dest_langs:
            if not lang.replace(" ", "").isalpha():
                raise ValueError(f"Destination language '{lang}' is not valid.")

        # Create language name → code lookup
        lang_lookup = {name.lower(): code for code, name in LANGUAGES.items()}

        # Handle auto-detect case
        if src == 'unknown':
            src_code = 'auto'
            src_name = 'Auto-Detect'

        else:
            src_code = lang_lookup.get(src)
            src_name = LANGUAGES.get(src_code)
            if not src_code or not src_name:
                raise ValueError(f"Could not find language: {src}")

        # Convert destination names to codes
        dest_codes = []
        dest_names = []

        for d in dest_langs:
            code = lang_lookup.get(d)
            name = LANGUAGES.get(code)
            if code and name:
                dest_codes.append(code)
                dest_names.append(name)
            else:
                raise ValueError(f"Could not recognize language: {d}")

        # Return everything
        return src_code, src_name, dest_codes, dest_names

    except Exception as e:
        print(f"{RED}Format Error:{RESET} {ORANGE}{e}{RESET}")
        return None, None, None, None


def autolookup(src):
    try:
        print("\nLooking up language for possible match....")
        trans = Translator()
        lang_match = trans.detect(src)
        detected_code = lang_match.lang

        src_name = LANGUAGES.get(detected_code)
        print(f"This looks like {src_name.capitalize()}. Using that....\n")

        return detected_code, src_name


    except Exception as e:
        error_msg(e)


def main():
    # sc : source language code (e.g. en, de, es)
    # sfn : source full name (e.g English, German, Spanish)
    # dc : Destination language code
    # dfn : Destination full name
    try:
        while True:
            # Get input in the form "English > German, French"
            raw = disp_console.input(
                "Enter languages to translate (e.g. \"English > German, French\"). "
                "Use 'Unknown' if you don't know the source language.\n>> "
            )

            # Run format check + language lookup
            sc, sfn, dc_list, dfn_list = formatcheck(raw)

            # If all language lookups succeed, continue
            if dc_list is not None:
                break

        # Ask user for the phrase to translate or translate a batch
        mode = disp_console.input("Press 1 to enter a batch of phrase or any other key to enter a single phrase: ")

        if mode.strip() == "1":
            phrase = disp_console.input("Enter a phrase to translate. Type \"END\" to submit:\n>> ")
            batch_obj = []

            while True:
                if phrase.strip().lower() == 'end':
                    break
                batch_obj.append(phrase)
                phrase = input(">>")

            if batch_obj:
                #Here we loop through the list of destination language codes  and create and object for each one
                #We then pass the batch of sentences to the batch_translation()
                for i in range(len(dc_list)):
                    my_translator = PocketTranslator(batch_obj, sc, sfn, dc_list[i], dfn_list[i])

                    results = my_translator.batch_translation(batch_obj)

                    print(f"\n{dfn_list[i].upper()} TRANSLATIONS:")
                    for r in results:
                        print(f"\nOriginal: {r['original']}")
                        print(f"Translated: {r['translated']}")
                return
            else:
                raise ValueError("Batch list is empty")
        else:
            phrase = disp_console.input("Enter a phrase to translate:\n>> ")

        # If multiple destinations were given, loop through all
            for i in range(len(dc_list)):
                my_translator = PocketTranslator(phrase, sc, sfn, dc_list[i], dfn_list[i])
                my_translator.basic_translate()

    except Exception as e:
        error_msg(e)


if __name__ == '__main__':
    main()
