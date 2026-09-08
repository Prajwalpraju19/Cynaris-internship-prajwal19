import pandas as pd

# 1. Load CSV into DataFrame
df = pd.read_csv("sales result.csv")


print(df)


# 2. Inspect the data

print(df.head())


df.info()


print(df.describe())


print(df["category"].value_counts())


# 3. Filter rows


electronics = df[df["category"] == "Electronics"]
print(electronics)


bangalore = df[df["city"] == "Bangalore"]
print(bangalore)


# Select columns

print("\n===== SELECTED COLUMNS =====")
selected = df[["customer_name", "product", "price", "city"]]
print(selected)


# Handle missing values


print(df.isnull().sum())

df["city"] = df["city"].fillna("Unknown")
df["category"] = df["category"].fillna("Unknown")


# 4. Group by and aggregate



category_summary = df.groupby("category").agg(
    total_quantity=("quantity", "sum"),
    average_price=("price", "mean"),
    total_sales=("price", "sum")
).reset_index()

print(category_summary)


# 5. Export cleaned data to CSV

df.to_csv("cleaned_sales.csv", index=False)

print("\n===== DONE =====")
print("Cleaned data exported to cleaned_sales.csv")