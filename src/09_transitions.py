import sys
import pandas as pd

page = sys.argv[1]
df = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
df = df.sort_values(["user_id", "timestamp", "row_id"])
df["prev"] = df.groupby("user_id")["event"].shift()
df["next"] = df.groupby("user_id")["event"].shift(-1)

d = df[df.event == page]
print("PREVIOUS:\n", d[d.prev != page]["prev"].value_counts(dropna=False, normalize=True).head(5).round(2))
print("NEXT:\n", d[d.next != page]["next"].value_counts(dropna=False, normalize=True).head(5).round(2))