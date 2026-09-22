"""
This is the bootstrap file to start the entire process in helper.py. DO NOT DELETE OR EDIT!
"""

import sys
import subprocess
import importlib


#This ensures mandatory libaries such as Rich are already installed in any case
def require(import_name, pip_name=None):
    pip_name = pip_name or import_name

    try:
        return importlib.import_module(import_name)

    except ModuleNotFoundError:
        print(f"[!] Missing '{import_name}'. Installing...")

        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            pip_name
        ])

        return importlib.import_module(import_name)
