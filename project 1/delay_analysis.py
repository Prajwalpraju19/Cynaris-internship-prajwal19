import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Project folder
BASE_DIR = Path(__file__).resolve().parent

# Load data
file_path = BASE_DIR / "da_journey_times.csv"
df = pd.read_csv(file_path)

print("Data loaded successfully!")
print("Rows:", len(df))

# -------------------------------------------------
# 1. Basic delay analysis
# -------------------------------------------------

print("\nAverage delay percentage:")
print(round(df["delay_pct"].mean(), 2), "%")

print("\nMedian delay percentage:")
print(round(df["delay_pct"].median(), 2), "%")

# -------------------------------------------------
# 2. Average delay by route
# -------------------------------------------------

route_delay = (
    df.groupby("route_id")["delay_pct"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTop 10 routes with highest average delay:")
print(route_delay.head(10))

# Save route delay results
route_delay_df = route_delay.reset_index()
route_delay_df.columns = ["route_id", "average_delay_pct"]

route_delay_df.to_csv(
    BASE_DIR / "route_delay_analysis.csv",
    index=False
)

# -------------------------------------------------
# 3. Average delay by hour
# -------------------------------------------------

hour_delay = (
    df.groupby("hour_of_day")["delay_pct"]
    .mean()
    .sort_index()
)

print("\nAverage delay by hour:")
print(hour_delay)

# -------------------------------------------------
# 4. Create delay heatmap
# -------------------------------------------------

heatmap_data = df.pivot_table(
    index="route_id",
    columns="hour_of_day",
    values="delay_pct",
    aggfunc="mean"
)

plt.figure(figsize=(16, 12))

sns.heatmap(
    heatmap_data,
    annot=False,
    cmap="YlOrRd",
    linewidths=0.3
)

plt.title("Average Transport Delay by Route and Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Route ID")

plt.tight_layout()

# Save heatmap
plt.savefig(
    BASE_DIR / "delay_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nDelay heatmap saved successfully!")

# -------------------------------------------------
# 5. Peak-hour analysis
# -------------------------------------------------

peak_hours = (
    df.groupby("hour_of_day")["delay_pct"]
    .mean()
    .sort_values(ascending=False)
)

print("\nTop 5 hours with highest average delay:")
print(peak_hours.head(5))

# -------------------------------------------------
# 6. High-delay + high-ridership routes
# -------------------------------------------------

route_performance = (
    df.groupby("route_id")
    .agg(
        average_delay_pct=("delay_pct", "mean"),
        average_passengers=("passenger_count", "mean"),
        average_stops=("stops_count", "mean")
    )
    .sort_values(
        "average_delay_pct",
        ascending=False
    )
)

print("\nTop 10 high-delay routes:")
print(route_performance.head(10))

route_performance.to_csv(
    BASE_DIR / "route_performance.csv"
)

print("\nAnalysis completed successfully!")