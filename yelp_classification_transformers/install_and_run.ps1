Write-Host "Creating virtual environment..."
python -m venv venv
venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Installation complete"

Write-Host "Running program..."
python driver.py
