"""
Single entry point for the Yelp classification project.

This driver uses the existing project files rather than duplicating their code.
"""
from helper import execute
from pathlib import Path
import os
import pandas as pd
from yelp import data_prep
from report import analysis_report



PROJECT_DIR = Path(__file__).resolve().parent
os.chdir(PROJECT_DIR)


def load_analysis_data():
    """
    Use the project's existing sample data for the analysis report.

    samples_cleaned.csv contains the cuisine and price-range values 
    """
    return pd.read_csv(PROJECT_DIR / "samples_cleaned.csv")


def main():
    print("\n--- Generating analysis report ---")
    frame = load_analysis_data()
    analysis_report(frame)

    print("\n--- Training model ---")
    # Import here so the analysis portion can run before the heavier
    # Transformers/PyTorch modules are loaded.
    from model_build import main as build_model
    build_model()

    print("\n[✓] Project completed.")


if __name__ == "__main__":
    execute(main)
