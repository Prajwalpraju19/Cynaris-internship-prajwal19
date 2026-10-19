import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load journey-time data
df = pd.read_csv(
    "UrbanMobility-Transit-Analytics/outputs/cleaned_da_journey_times.csv"
)

# Create output folder
os.makedirs("UrbanMobility-Transit-Analytics/outputs", exist_ok=True)

# Check delay statistics
print("Average delay:", round(df["delay_min"].mean(), 2), "minutes")
print("Maximum delay:", df["delay_min"].max(), "minutes")
print("Average delay percentage:", round(df["delay_pct"].mean(), 2), "%")

# Calculate average delay for each route and hour
heatmap_data = df.pivot_table(
    index="route_id",
    columns="hour_of_day",
    values="delay_min",
    aggfunc="mean"
)

# Create heatmap
plt.figure(figsize=(16, 8))

sns.heatmap(
    heatmap_data,
    cmap="YlOrRd",
    annot=True,
    fmt=".1f",
    linewidths=0.3
)

plt.title("UrbanMobility - Average Bus Delay by Route and Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Bus Route")
plt.tight_layout()

# Save image
plt.savefig(
    "UrbanMobility-Transit-Analytics/outputs/delay_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nHeatmap saved successfully!")
plt.show()