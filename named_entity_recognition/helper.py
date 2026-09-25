"""
This is boiler code for different system helper functions frequently used in various projects
"""

import sys
import traceback
import os
import signal

from bootstrap import require

rich = require("rich")
from rich.console import Console

from rich.progress import (
    Progress as RichProgress,
    SpinnerColumn,
    TextColumn,
)
##################### Setup Functions #####################



'''

NOTE: These are backup ANSI color codes if the Rich library is not working
-- This sets the system colors --
GREEN = '\u001b[92m'
RED = '\u001b[91m'
ORANGE = '\u001b[38;5;208m'
RESET = '\u001b[0m'
'''

# -- -------Functions from "Rich" Library ---------------#

console = Console()

def progress(**kwargs):
    return RichProgress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    )


## -------------Console Message Handling-----------------------##

def mod_not_found(mod):
    console.print(f"[red]ERROR[/red]: [orange1]{mod} was not found. \
                  Check the requirements.txt to be sure it has been included[/orange1]")

def error_msg(e):
    console.print(f"[red]Error:[/red] [orange1]{e}[/orange1]")
    traceback.print_exc()
    sys.exit(1)



def silence():  # This is for when the console is complaining about something petty
    sys._stderr = sys.stderr  # Backup just once
    sys.stderr = open(os.devnull, 'w')


def restore_sanity():  # This restores error output after being silenced
    if hasattr(sys, '_stderr'):
        sys.stderr = sys._stderr  # Restore
        del sys._stderr

def sigint_handler(signum, frame):
    print("\nTerminating program...\n")
    raise SystemExit(0)


def terminate_signal():
    signal.signal(signal.SIGINT, sigint_handler)

def hf_silence(): #This silences Hugging Face log messages

    try:
        from huggingface_hub.utils import disable_progress_bars
        from huggingface_hub import logging as hf_logging
    except ModuleNotFoundError:
        disable_progress_bars = None #If these modules are not necessary for the project, they are ignored
        hf_logging = None
        mod_not_found("Hugging Face")
        

    if hf_logging is not None:
        hf_logging.set_verbosity_error()

    if disable_progress_bars is not None:
        disable_progress_bars()

def ds_logger_silence():
    try:
        from datasets import logging
    except ModuleNotFoundError:
        logging = None
        mod_not_found("Datasets")
    if logging is not None:
        logging.set_verbosity_error()


  ############ Silencing interface ##################

def silencer(*args):
    for arg in args:
        match arg:
            case "hf":
                hf_silence()
            case "ds_logger":
                ds_logger_silence()
            case "console":
                silence() #Remember to restore_sanity()!


#########################################################


#----- Main executor function module --------------#
def execute(func):
    try:
        func()
    except KeyboardInterrupt:
        print("Terminating program...")
        raise SystemExit(0)
    except Exception as e:
        error_msg(e)

