import pandas as pd
import os

# Create outputs folder
os.makedirs("UrbanMobility-Transit-Analytics/outputs", exist_ok=True)

# Load all datasets
files = [
    "da_bus_routes.csv",
    "da_journey_times.csv",
    "da_ridership_data.csv"
]

for file in files:
    df = pd.read_csv("UrbanMobility-Transit-Analytics/data/" + file)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Check missing values
    print("\nDataset:", file)
    print(df.isnull().sum())

    # Save cleaned dataset
    df.to_csv(
        "UrbanMobility-Transit-Analytics/outputs/cleaned_" + file,
        index=False
    )

    print("Saved successfully!")

print("\nAll datasets processed!")




