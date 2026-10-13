import pandas as pd
from pathlib import Path

# Get the folder containing this Python file
BASE_DIR = Path(__file__).resolve().parent

# Load bus route data
csv_path = BASE_DIR / "da_bus_routes.csv"

print("Looking for:", csv_path)
print("File exists:", csv_path.exists())

# Read CSV
routes = pd.read_csv(csv_path)

print("\nCSV loaded successfully!")

print("\nDataset shape:")
print(routes.shape)

print("\nColumn names:")
print(routes.columns.tolist())

print("\nFirst 5 rows:")
print(routes.head())