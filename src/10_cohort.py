import pandas as pd

df = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
df = df.sort_values(["user_id", "timestamp", "row_id"])

cohort = (df[df.event == "registration"]
          .groupby("user_id")["timestamp"].min()
          .rename("entry_ts").to_frame())

first_event = df.groupby("user_id").head(1).set_index("user_id")["event"]
cohort["registration_first"] = first_event.reindex(cohort.index).eq("registration")

m = df.merge(cohort[["entry_ts"]], left_on="user_id", right_index=True)
login_before = m[(m.event == "login") & (m.timestamp < m.entry_ts)]["user_id"].unique()
cohort["login_before"] = cohort.index.isin(login_before)

end = df["timestamp"].max()
cohort["full_window"] = cohort["entry_ts"] <= end - pd.Timedelta(days=7)

print(len(cohort), cohort.registration_first.sum(),
      cohort.login_before.sum(), cohort.full_window.sum())
cohort.to_csv("data/processed/cohort.csv")