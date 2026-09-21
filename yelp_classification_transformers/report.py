"""
Generate the Yelp analysis report.

The functions here intentionally stay separate from the training code.
The driver imports this module and passes it a prepared DataFrame.
"""

import io
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def prepare_analysis_data(frame):
    """Add the sentiment column for analysis."""
    df = frame.copy()

    # Yelp Review Full labels are 0-4.
    sentiment_map = {
        0: "negative",
        1: "negative",
        2: "neutral",
        3: "positive",
        4: "positive",
    }

    if "sentiment" not in df.columns:
        df["sentiment"] = df["label"].map(sentiment_map)

    return df


def _percent_table(frame, row, column):
    """Return row percentages for a two-way categorical comparison."""
    table = pd.crosstab(frame[row], frame[column], normalize="index") * 100
    return table


def analysis_report(frame, output_file="analysis_report.txt", show_plots=True):
    """
    Print the analysis, save the same text to a report file,
    and display the charts used in the original analysis.
    """
    df = prepare_analysis_data(frame)

    required = {"label", "text", "sentiment", "cuisine", "price_range"}
    missing = required.difference(df.columns)

    if missing:
        raise ValueError(
            "Analysis data is missing required columns: "
            + ", ".join(sorted(missing))
        )

    output = io.StringIO()

    def report_print(*args, **kwargs):
        print(*args, **kwargs)
        print(*args, **kwargs, file=output)

    report_print("YELP DATA ANALYSIS")
    report_print("=" * 70)

    # Q1
    report_print("\nQ1: Analyze the basic statistics of your dataset")
    report_print("-" * 70)
    report_print(df.head())
    report_print("\nLabel distribution:")
    report_print(df["label"].value_counts().sort_index())
    report_print("\nBasic statistics:")
    report_print(df.describe(include="all"))

    # Q2
    report_print("\nQ2: Analyze the data structure")
    report_print("-" * 70)

    info_buffer = io.StringIO()
    df.info(buf=info_buffer)
    report_print(info_buffer.getvalue())

    # Q3
    report_print("\nQ3: Create a pie chart of the sentiment distribution")
    report_print("-" * 70)
    sentiment_counts = df["sentiment"].value_counts()
    sentiment_percent = df["sentiment"].value_counts(normalize=True) * 100
    report_print(sentiment_counts)
    report_print("\nPercentages:")
    report_print(sentiment_percent.round(2))

    sentiment_counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        ylabel="",
        title="Sentiment Distribution",
    )
    plt.tight_layout()
    if show_plots:
        plt.show()
    else:
        plt.close()

    # Q4
    report_print("\nQ4: Analyze sentiment patterns across different cuisines")
    report_print("-" * 70)
    cuisine_sentiment = _percent_table(df, "cuisine", "sentiment")
    report_print(cuisine_sentiment.round(2))

    cuisine_sentiment.plot(
        kind="bar",
        stacked=True,
        title="Sentiment Distribution by Cuisine",
    )
    plt.ylabel("Percentage")
    plt.xlabel("Cuisine")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if show_plots:
        plt.show()
    else:
        plt.close()

    # Q5
    report_print("\nQ5: Analyze sentiment patterns across price ranges")
    report_print("-" * 70)
    price_sentiment = _percent_table(df, "price_range", "sentiment")
    report_print(price_sentiment.round(2))

    price_sentiment.plot(
        kind="bar",
        stacked=True,
        title="Sentiment Distribution by Price Range",
    )
    plt.ylabel("Percentage")
    plt.xlabel("Price Range")
    plt.xticks(rotation=0)
    plt.tight_layout()
    if show_plots:
        plt.show()
    else:
        plt.close()

    # The original PDF jumps from Q5 to Q7, so this keeps the same numbering.

    # Q7
    report_print(
        "\nQ7: Analyze the relationship between cuisine types "
        "and price ranges using a heatmap"
    )
    report_print("-" * 70)
    cuisine_price = _percent_table(df, "cuisine", "price_range")
    report_print(cuisine_price.round(2))

    plt.figure(figsize=(8, 6))
    sns.heatmap(cuisine_price, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("Cuisine Type vs. Price Range")
    plt.xlabel("Price Range")
    plt.ylabel("Cuisine")
    plt.tight_layout()
    if show_plots:
        plt.show()
    else:
        plt.close()

    # Q8
    report_print("\nQ8: Summary")
    report_print("-" * 70)
    report_print(
        f"The dataset contains {len(df):,} reviews. "
        "The label distribution, sentiment distribution, cuisine/sentiment "
        "comparison, price/sentiment comparison, and cuisine/price "
        "relationship are shown above."
    )

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(output.getvalue())

    print(f"\n[✓] Report written to {output_file}")

def main():
    frame = pd.read_csv("samples_cleaned.csv")
    analysis_report(frame)
