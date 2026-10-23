from pathlib import Path
import pandas as pd
from autoviz.AutoViz_Class import AutoViz_Class
import sweetviz as sv

# Find the CSV file in the current project folder
csv_files = list(Path(".").glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "Place your retail dataset CSV in this project folder."
    )

data_file = csv_files[0]
print(f"Dataset: {data_file}")

df = pd.read_csv(data_file)
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())
print("\nMissing values:")
print(df.isnull().sum())

# Run AutoViz and export its visualizations
AV = AutoViz_Class()
AV.AutoViz(
    filename=str(data_file),
    sep=",",
    depVar="",
    dfte=None,
    header=0,
    verbose=1,
    lowess=False,
    chart_format="html",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
)

# Run SweetViz and save the HTML report
report = sv.analyze(df)
report.show_html(
    filepath="sweetviz_report.html",
    open_browser=False
)

print("Analysis completed.")
print("Check the project folder for the HTML reports.")
