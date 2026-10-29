import pandas as pd

df = pd.read_csv("data/processed/events_dedup.csv", usecols=["user_id"])
users = df.groupby("user_id").size().rename("n_events").reset_index()

threshold = users["n_events"].quantile(0.999)
users["heavy_user"] = users["n_events"] > threshold

print(f"threshold={threshold:.1f}, flagged={users['heavy_user'].sum()}, "
      f"share_of_events={users.loc[users.heavy_user, 'n_events'].sum() / users['n_events'].sum():.3f}")
users.to_csv("data/processed/user_flags.csv", index=False)