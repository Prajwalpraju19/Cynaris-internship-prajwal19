
import os
import time
import statistics

import pandas as pd
import duckdb
import polars as pl

# -------------------------------
# 1. Create folders and sample CSV
# -------------------------------
os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

CSV_FILE = "data/transit_100k.csv"

if not os.path.exists(CSV_FILE):
    print("Generating a 100,000-row sample dataset...")

    sample = pd.DataFrame({
        "route_id": [
            f"R{(i % 30) + 1:02d}" for i in range(100_000)
        ],
        "hour": [(i % 24) for i in range(100_000)],
        "delay_min": [
            (i * 7 % 41) for i in range(100_000)
        ],
        "passenger_count": [
            (i * 13 % 101) + 1 for i in range(100_000)
        ],
        "time_category": [
            "Peak" if 7 <= (i % 24) <= 10
            or 17 <= (i % 24) <= 20
            else "Off-Peak"
            for i in range(100_000)
        ]
    })

    sample.to_csv(CSV_FILE, index=False)

# -------------------------------
# 2. Load the same CSV
# -------------------------------
print("\nLoading dataset...")

start = time.perf_counter()
pdf = pd.read_csv(CSV_FILE)
pandas_load = time.perf_counter() - start

start = time.perf_counter()
con = duckdb.connect()
con.execute("""
    CREATE TABLE transit AS
    SELECT * FROM read_csv_auto(?)
""", [os.path.abspath(CSV_FILE)])
duckdb_load = time.perf_counter() - start

start = time.perf_counter()
pldf = pl.read_csv(CSV_FILE)
polars_load = time.perf_counter() - start

print(f"Rows loaded: Pandas={len(pdf):,}, "
      f"DuckDB={con.execute('SELECT COUNT(*) FROM transit').fetchone()[0]:,}, "
      f"Polars={pldf.height:,}")

# -------------------------------
# 3. Five equivalent operations
# -------------------------------
pandas_queries = [
    lambda: pdf.groupby("route_id")["delay_min"].mean(),
    lambda: pdf.groupby("time_category").size(),
    lambda: pdf.groupby("route_id")["passenger_count"]
                 .sum().sort_values(ascending=False).head(10),
    lambda: pdf.groupby("hour")["delay_min"].mean(),
    lambda: pdf[pdf["delay_min"] > 15]
]

duckdb_queries = [
    "SELECT route_id, AVG(delay_min) AS avg_delay FROM transit GROUP BY route_id",
    "SELECT time_category, COUNT(*) AS total FROM transit GROUP BY time_category",
    """SELECT route_id, SUM(passenger_count) AS total_passengers
       FROM transit GROUP BY route_id
       ORDER BY total_passengers DESC LIMIT 10""",
    "SELECT hour, AVG(delay_min) AS avg_delay FROM transit GROUP BY hour ORDER BY hour",
    "SELECT * FROM transit WHERE delay_min > 15"
]

polars_queries = [
    lambda: pldf.group_by("route_id").agg(
        pl.col("delay_min").mean().alias("avg_delay")
    ),
    lambda: pldf.group_by("time_category").len(),
    lambda: pldf.group_by("route_id").agg(
        pl.col("passenger_count").sum().alias("total_passengers")
    ).sort("total_passengers", descending=True).head(10),
    lambda: pldf.group_by("hour").agg(
        pl.col("delay_min").mean().alias("avg_delay")
    ).sort("hour"),
    lambda: pldf.filter(pl.col("delay_min") > 15)
]

query_names = [
    "Average delay by route",
    "Trips by time category",
    "Top 10 routes by passengers",
    "Average delay by hour",
    "Filter delay above 15 minutes"
]

# -------------------------------
# 4. Benchmark each operation
# -------------------------------
def benchmark(function, repeats=3):
    # First run warms up the operation.
    function()

    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        times.append(time.perf_counter() - start)

    return round(statistics.median(times) * 1000, 3)

rows = []

for i, name in enumerate(query_names):
    pandas_ms = benchmark(pandas_queries[i])

    duckdb_ms = benchmark(
        lambda q=duckdb_queries[i]: con.execute(q).fetchdf()
    )

    polars_ms = benchmark(polars_queries[i])

    rows.append({
        "Operation": name,
        "Pandas_ms": pandas_ms,
        "DuckDB_ms": duckdb_ms,
        "Polars_ms": polars_ms
    })

# -------------------------------
# 5. Save results
# -------------------------------
results = pd.DataFrame(rows)
results.to_csv("results/benchmark_results.csv", index=False)

comparison = pd.DataFrame([
    ["Ease of use", "Beginner-friendly Python",
     "SQL-based analytics", "Expression-based Python"],
    ["Query language", "Python API", "SQL",
     "Python API / expressions"],
    ["Large CSV analytics", "Good", "Very good for SQL analytics",
     "Very good"],
    ["Memory approach", "Usually loads data into memory",
     "Can process queries without materializing all results in Pandas",
     "Columnar, often memory-efficient"],
    ["Best use case", "General data analysis",
     "SQL analytics on files and tables",
     "Fast DataFrame transformations"]
], columns=[
    "Criterion", "Pandas", "DuckDB", "Polars"
])

comparison.to_csv("results/comparison_table.csv", index=False)

print("\n--- Benchmark Results (median milliseconds) ---")
print(results.to_string(index=False))

print("\n--- Comparison Table ---")
print(comparison.to_string(index=False))

print("\nSaved:")
print("results/benchmark_results.csv")
print("results/comparison_table.csv")

con.close()
