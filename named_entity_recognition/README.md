# Named Entity Recognition Demonstration

An educational **Named Entity Recognition (NER)** project built with spaCy. It runs a pretrained English NER pipeline over a technology-news corpus, displays the entities it finds, produces label-distribution charts, and prints comparison-oriented diagnostics against a supplied annotation file.

This repository is designed to demonstrate an end-to-end NLP workflow: loading a language model, extracting structured information from unstructured text, transforming results into a DataFrame, and communicating findings with console reports and visualizations.

> **Scope:** This project uses spaCy's pretrained `en_core_web_sm` pipeline. It demonstrates NER inference and analysis; it does **not** train a custom NER model.

## What it does

- Loads spaCy's English small pipeline: `en_core_web_sm`
- Reads `tech_news_mashup.txt`, a technology-news text corpus
- Extracts entities such as people, organizations, locations, dates, money values, and facilities
- Prints a readable table containing each entity, its spaCy label, and the label description
- Produces four interactive Matplotlib/Seaborn charts:
  - entity-label bar chart
  - single-token-only entity-label bar chart
  - entity-label pie chart
  - single-token-only entity-label pie chart
- Groups infrequent labels into **Other** for clearer visual summaries
- Prints comparison-oriented precision, recall, F1, false-positive, and false-negative diagnostics

## Project structure

| File | Purpose |
| --- | --- |
| `driver.py` | Main program: model loading, extraction, analysis, evaluation output, and charts |
| `helper.py` | Shared console, error-handling, dependency, and Ctrl+C helpers |
| `bootstrap.py` | Lightweight helper for importing required runtime packages |
| `tech_news_mashup.txt` | Technology-news corpus analysed by the program |
| `spacy_sample_text.txt` | Short standalone text sample for experimenting with spaCy NER |
| `gold_entities.json` | Supplied entity annotations used by the diagnostic comparison code |
| `requirements.txt` | Pinned Python dependencies, including the compatible spaCy English model |
| `install_and_run.bat` / `install_and_run.sh` | Windows and Bash convenience setup scripts |

## Requirements

- Python 3.10 or 3.11
- Internet access for the initial package installation
- A graphical desktop session so Matplotlib can display the charts

The project is CPU-friendly; a GPU is not required.

## Installation and usage

Run the commands from the `named_entity_recognition` directory. This matters because the program reads its input files using relative paths.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python driver.py
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python driver.py
```

The program prints the detected entities and diagnostic summaries in the terminal, then opens the charts in separate windows. Press **Enter** in the terminal after reviewing the charts to close the program.

## Interpreting the output

spaCy assigns labels to entity spans. Common labels in this demonstration include:

| Label | Meaning |
| --- | --- |
| `PERSON` | A named individual or fictional character |
| `ORG` | An organization, company, agency, or institution |
| `GPE` | A country, city, state, or other geopolitical entity |
| `DATE` | An absolute or relative date or period |
| `MONEY` | A monetary amount, including its currency |
| `FAC` | A building, airport, highway, bridge, or similar facility |

The raw console table preserves the model's individual predictions. The visualizations then summarize label frequencies. The single-token view is a separate presentation filter; it excludes multiword entity strings such as company names or multiword locations.

## Important note about the evaluation diagnostics

The project includes `gold_entities.json` and reports precision, recall, and F1-style diagnostics. Those numbers are useful for demonstrating set comparison, normalization, and error reporting, but they are **not a formal benchmark score** for the analysed news corpus:

- `tech_news_mashup.txt` and the supplied gold JSON are not aligned document-for-document.
- The current comparison normalizes entity text and labels into sets, so it does not preserve every occurrence or validate exact character spans.

A production-quality NER evaluation should use held-out documents paired with their own annotations and score exact `(start_char, end_char, label)` matches. Until that is implemented, treat the displayed metrics as diagnostic demonstrations rather than claims about the pretrained model's real-world accuracy.

## Reproducibility

The dependency versions are pinned deliberately. In particular, the project includes the spaCy model as a direct requirement so a fresh environment receives both spaCy and `en_core_web_sm`.

After installing the requirements, confirm that the model is available:

```bash
python -c "import spacy; print(spacy.load('en_core_web_sm').pipe_names)"
```

## Technologies

- Python
- spaCy
- pandas
- NumPy
- Matplotlib
- Seaborn
- scikit-learn
- Rich
- tabulate
