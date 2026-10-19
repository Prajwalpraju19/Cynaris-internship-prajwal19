
import os
import logging
import pandas as pd
from dotenv import load_dotenv
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI

# Configure error logging
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


def safe_query(question, smart_df):
    """Run a PandasAI query and log any errors."""
    try:
        answer = smart_df.chat(question)
        print(f"\nQuestion: {question}")
        print(f"Answer: {answer}")
        return answer

    except Exception:
        logging.exception("PandasAI query failed: %s", question)
        print(f"Query failed. Check error.log: {question}")
        return None


def main():
    try:
        # 1. Load the Indian retail dataset
        csv_file = "india_retail_sales_dataset.csv"

        if not os.path.exists(csv_file):
            raise FileNotFoundError(
                f"Dataset not found: {csv_file}. "
                "Place the CSV in the same folder as this script."
            )

        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip()

        print("Dataset loaded successfully!")
        print("Dataset shape:", df.shape)
        print("Columns:", df.columns.tolist())
        print("\nFirst five rows:")
        print(df.head())

        # 2. Configure PandasAI
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to your .env file."
            )

        llm = OpenAI(api_token=api_key)
        smart_df = SmartDataframe(df, config={"llm": llm})

        # 3. Run 10 natural-language questions
        questions = [
            "Summarize this dataset.",
            "How many records are present?",
            "Are there any missing values?",
            "What are the numerical columns?",
            "Show descriptive statistics.",
            "Which state has the highest sales?",
            "Which product category has the highest sales?",
            "What is the total sales amount?",
            "Which city has the highest sales?",
            "Identify unusual values or possible outliers."
        ]

        query_results = []

        for number, question in enumerate(questions, start=1):
            print(f"\n--- Query {number}/10 ---")
            answer = safe_query(question, smart_df)

            query_results.append({
                "question_number": number,
                "question": question,
                "answer": str(answer) if answer is not None else "FAILED"
            })

        pd.DataFrame(query_results).to_csv(
            "query_results.csv", index=False
        )

        # 4. Compare PandasAI and manual Pandas for 3 questions
        print("\n--- PandasAI vs Manual Pandas ---")

        comparisons = []

        def compare(question, manual_result, ai_result):
            comparisons.append({
                "question": question,
                "manual_pandas": str(manual_result),
                "pandasai": str(ai_result)
                if ai_result is not None else "FAILED",
                "accuracy_review": "PENDING MANUAL VERIFICATION"
            })

        # Question 1: Record count
        q1 = "How many records are present?"
        ai1 = safe_query(q1, smart_df)
        compare(q1, len(df), ai1)

        # Question 2: Missing values
        q2 = "Are there any missing values?"
        manual_missing = df.isnull().sum().to_dict()
        ai2 = safe_query(q2, smart_df)
        compare(q2, manual_missing, ai2)

        # Question 3: Descriptive statistics
        q3 = "Show descriptive statistics."
        manual_stats = df.describe().round(2).to_dict()
        ai3 = safe_query(q3, smart_df)
        compare(q3, manual_stats, ai3)

        pd.DataFrame(comparisons).to_csv(
            "comparison_results.csv", index=False
        )

        # 5. Display final results
        print("\n--- Manual Pandas Results ---")
        print("Record count:", len(df))
        print("\nMissing values:")
        print(df.isnull().sum())
        print("\nDescriptive statistics:")
        print(df.describe())

        print("\nAll processing steps completed.")
        print("Files created:")
        print("- query_results.csv")
        print("- comparison_results.csv")
        print("- error.log (if errors occur)")

    except Exception:
        logging.exception("Analysis setup or execution failed")
        print("Analysis failed. Check error.log for details.")


if __name__ == "__main__":
    main()
