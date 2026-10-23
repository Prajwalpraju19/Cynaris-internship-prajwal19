
import os
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# Folder containing this Python file
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "india_retail_sales_dataset.csv"

# Store errors in this folder
LOG_FILE = BASE_DIR / "error.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv(BASE_DIR / ".env")


def main():
    # Load the dataset
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV not found: {CSV_FILE}\n"
            "Copy india_retail_sales_dataset.csv into this folder."
        )

    df = pd.read_csv(CSV_FILE)

    if df.empty:
        raise ValueError("The dataset contains no rows.")

    print("=" * 60)
    print("INDIAN RETAIL SALES - PANDASAI ANALYSIS")
    print("=" * 60)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Column names:", df.columns.tolist())
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    # Configure the language model
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to the .env file."
        )

    llm = OpenAI(api_token=api_key)
    smart_df = SmartDataframe(
        df.copy(),
        config={"llm": llm, "verbose": False},
    )

    # Ten natural-language questions
    questions = [
        "How many rows are present in this dataset?",
        "How many columns are present in this dataset?",
        "Show the first five records.",
        "What are the column names and data types?",
        "How many missing values are present in each column?",
        "How many duplicate rows are present?",
        "Give a statistical summary of the numeric columns.",
        "Which column has the most missing values?",
        "What are the five most frequent values in each text column?",
        "Summarize the important patterns and data quality issues in this dataset.",
    ]

    successful = 0
    failed = 0

    # Execute and handle each question separately
    for number, question in enumerate(questions, start=1):
        print(f"\n{'=' * 60}")
        print(f"QUERY {number}/10")
        print("Question:", question)

        try:
            answer = smart_df.chat(question)
            print("Answer:", answer)
            successful += 1

        except Exception:
            logging.exception(
                "Natural-language query %s failed: %s",
                number,
                question,
            )
            print("Query failed. See error.log for details.")
            failed += 1

    print(f"\n{'=' * 60}")
    print("QUERY SUMMARY")
    print("Successful queries:", successful)
    print("Failed queries:", failed)
    print("Total queries:", len(questions))
    print("Error log:", LOG_FILE)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Fatal error while running PandasAI analysis.")
        print(
            "\nAnalysis could not start. Check error.log "
            "and verify your CSV file and API key."
        )
