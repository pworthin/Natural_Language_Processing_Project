"""
This is boiler code for different system helper functions frequently used in various project
"""

import sys
import traceback
import os

from huggingface_hub.utils import disable_progress_bars
from huggingface_hub import logging as hf_logging


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

# -- Functions from "Rich" Library --#

console = Console()

def progress(**kwargs):
    return RichProgress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    )

###---------------------------------##


## ---- Hugging Face Options ---- ##
def hf_silence(): #This silences Hugging Face log messages
    hf_logging.set_verbosity_error()
    disable_progress_bars()


## -------------------------------##


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


#########################################################


def execute(func):
    try:
        func()
    except KeyboardInterrupt:
        print("Terminating program...")
        raise SystemExit(0)
    except Exception as e:
        error_msg(e)