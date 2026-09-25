# Natural Language Processing Projects

A small collection of Python projects created to demonstrate practical familiarity with core Natural Language Processing (NLP) workflows: classical text classification, named entity recognition, transformer-based sequence classification, exploratory data analysis, and reproducible project setup.

These are **educational and portfolio demonstrations**, not production services. They prioritize making the concepts, pipeline stages, and results visible and inspectable. They are intentionally small in scope and should not be treated as deployed systems, benchmark implementations, or decision-making tools.

## Repository map

| Project | Concepts demonstrated | Main technologies |
| --- | --- | --- |
| [Named Entity Recognition](named_entity_recognition/) | Entity extraction, linguistic labels, tabular reporting, visual summaries, diagnostic evaluation | spaCy, pandas, Matplotlib, Seaborn |
| [Movie Review Sentiment Analysis](sentiment_analysis/) | Text preprocessing, bag-of-words and TF-IDF features, model comparison, classification reports | NLTK, scikit-learn, pandas |
| [Yelp Review Analysis and Transformer Utilities](yelp_classification_transformers/) | Hugging Face datasets, DistilBERT sequence-classification utilities, GPU-aware inference, exploratory review analysis and reporting | Transformers, PyTorch, datasets, pandas, Seaborn |

Each project is self-contained and has its own dependencies and run instructions. Open the project's directory and README before installing or running it.

## What this repository demonstrates

- Turning unstructured text into features or structured entities
- Working with standard NLP datasets and pretrained language models
- Comparing baseline classification approaches instead of assuming one algorithm is magically best
- Separating orchestration, data preparation, model logic, reporting, and shared helpers
- Producing interpretable terminal output and visualizations
- Using virtual environments, dependency files, and platform-specific setup scripts

## Projects

### 1. Named Entity Recognition

The NER demonstration loads spaCy's pretrained `en_core_web_sm` English pipeline and analyses a technology-news corpus. It prints detected entity spans and their labels, then produces bar and pie charts that summarize the label distribution.

The project demonstrates inference with a pretrained model; it does **not** train a custom NER model. Its included precision/recall/F1-style output is a diagnostic comparison exercise, not a formal benchmark: the supplied annotation file is not aligned document-for-document with the analysed corpus, and the current comparison does not score exact character spans.

See the [project README](named_entity_recognition/README.md) for installation and a complete explanation.

### 2. Movie Review Sentiment Analysis

This project uses NLTK's `movie_reviews` corpus to compare four classical text-classification pipelines:

- CountVectorizer + Multinomial Naive Bayes
- CountVectorizer + Linear Support Vector Classifier
- TF-IDF Vectorizer + Multinomial Naive Bayes
- TF-IDF Vectorizer + Linear Support Vector Classifier

It downloads the required NLTK resources at runtime, shuffles the corpus, creates a reproducible train/test split, and reports accuracy plus per-class precision, recall, and F1.

This is a compact benchmark exercise intended to demonstrate the relationship between text representation and classifier choice—not a production sentiment API.

See the [project README](sentiment_analysis/README.md) for setup details.

### 3. Yelp Review Analysis and Transformer Utilities

This project explores the Hugging Face `Yelp/yelp_review_full` dataset and includes reusable utilities for fine-tuning and using DistilBERT sequence-classification models. It also generates an exploratory text report and charts for sentiment, cuisine, and price-range comparisons.

The default driver:

1. Loads the Yelp dataset.
2. Derives negative, neutral, and positive sentiment groups from the original 1–5-star labels.
3. Creates deterministic synthetic cuisine and price-range categories for the exploratory analysis.
4. Produces a console/text report, pie chart, stacked bar charts, and a heatmap.

The synthetic cuisine and price-range fields are **not verified Yelp attributes**. They exist solely to demonstrate categorical analysis, label encoding, reporting, and visualization techniques. The optional `model_build.py` and `predict.py` files demonstrate the mechanics of training and batch inference with local transformer model directories; they are not presented as validated restaurant-price or cuisine predictors.

See the [project README](yelp_classification_transformers/README.md) for the module-level setup notes.

## Running a project

Use a separate virtual environment for each subproject. From the repository root:

```bash
cd <project-directory>
```

Then follow that project's README and install its own `requirements.txt`. The repository includes helper scripts for Windows PowerShell, Windows batch, and Bash where applicable.

## Scope and limitations

These projects deliberately avoid claiming more than they demonstrate:

- No project is exposed as a web service or hardened for untrusted input.
- Dataset-derived labels, synthetic categories, and coursework metrics are not business truth.
- Pretrained model output can be wrong, biased, incomplete, or sensitive to context.
- Training and evaluation procedures are demonstrative unless a project explicitly documents a proper held-out, aligned test set.
- Dependency versions and setup instructions are included to support local reproduction, but may require adjustment on substantially newer Python or hardware stacks.

## Technologies

Python · spaCy · NLTK · scikit-learn · Hugging Face Transformers · PyTorch · datasets · pandas · NumPy · Matplotlib · Seaborn · Rich
