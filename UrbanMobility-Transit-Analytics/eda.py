import pandas as pd

# Load cleaned datasets
routes = pd.read_csv("UrbanMobility-Transit-Analytics/outputs/cleaned_da_bus_routes.csv")
journeys = pd.read_csv("UrbanMobility-Transit-Analytics/outputs/cleaned_da_journey_times.csv")
ridership = pd.read_csv("UrbanMobility-Transit-Analytics/outputs/cleaned_da_ridership_data.csv")

# Display dataset information
print("BUS ROUTES")
print(routes.head())
print(routes.info())

print("\nJOURNEY TIMES")
print(journeys.head())
print(journeys.info())

print("\nRIDERSHIP DATA")
print(ridership.head())
print(ridership.info())

# Summary statistics
print("\nRIDERSHIP SUMMARY")
print(ridership.describe())

print("\nJOURNEY TIME SUMMARY")
print(journeys.describe())