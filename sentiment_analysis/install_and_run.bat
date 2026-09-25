@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating environment...
call venv\Scripts\activate

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Running program...
python reviews.py

pause