import pandas as pd

data_url = "https://data.gov"

try:
    df = pd.read_csv(data_url)
    print("Successfully pulled NPS data")
except Exception as e:
    print(f"Error fetching data: {e}")
    raise SystemExit(1)

slbe_data = df[
    (df["ParkCode"] == "SLBE") & (df["Field"] == "Recreation Visitors")
]

monthly_averages = slbe_data.groupby("Month")["Value"].mean().to_dict()

max_visitors = max(monthly_averages.values())
slbe_weights = {
    month: value / max_visitors for month, value in monthly_averages.items()
}

print("Calculated monthly weights from web")
print(slbe_weights)
