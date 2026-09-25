#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running program..."
python reviews.py
