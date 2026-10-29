import pandas as pd

df = pd.read_csv("data/raw/e_wallet.csv", parse_dates=["timestamp"])
df["row_id"] = df.index          # original file order = our tie-break rule
n_before = len(df)

df = df.drop_duplicates(subset=["user_id", "timestamp", "event"], keep="first")
n_after = len(df)

removed = n_before - n_after
print(f"before={n_before}, after={n_after}, removed={removed} ({removed / n_before:.2%})")
df.to_csv("data/processed/events_dedup.csv", index=False)