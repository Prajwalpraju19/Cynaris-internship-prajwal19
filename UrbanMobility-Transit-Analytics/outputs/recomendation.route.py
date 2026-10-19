import pandas as pd

# Load datasets
journeys = pd.read_csv(
    "UrbanMobility-Transit-Analytics/outputs/cleaned_da_journey_times.csv"
)

ridership = pd.read_csv(
    "UrbanMobility-Transit-Analytics/outputs/cleaned_da_ridership_data.csv"
)

# 1. Average delay by route
print("\n1. ROUTES WITH HIGHEST AVERAGE DELAY")
print(
    journeys.groupby("route_id")["delay_min"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
)

# 2. Passenger demand by route
print("\n2. ROUTES WITH HIGHEST PASSENGER DEMAND")
print(
    ridership.groupby("route_id")["daily_passengers"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
)

# 3. Average delay by hour
print("\n3. HOURS WITH HIGHEST AVERAGE DELAY")
print(
    journeys.groupby("hour_of_day")["delay_min"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .round(2)
)

# 4. Passenger demand on weekends vs weekdays
print("\n4. WEEKEND VS WEEKDAY PASSENGERS")
print(ridership.groupby("is_weekend")["daily_passengers"].mean().round(2))

# 5. Average delay by peak/off-peak period
print("\n5. PEAK VS OFF-PEAK DELAY")
print(journeys.groupby("time_category")["delay_min"].mean().round(2))

print("\nAnalysis completed!")
