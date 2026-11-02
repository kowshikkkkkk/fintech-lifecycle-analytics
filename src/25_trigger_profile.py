import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
end = ev["timestamp"].max()
co = co[co.entry_ts + pd.Timedelta(days=10) <= end]

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp > m.entry_ts) & (m.event != "registration")]
m["day"] = ((m.timestamp - m.entry_ts) // pd.Timedelta(days=1)).astype(int)

day0 = m[m.day == 0]
day12 = set(m.loc[m.day.isin([1, 2]), "user_id"])
pop = set(day0.user_id) - day12
d = day0[day0.user_id.isin(pop)].sort_values(["user_id", "timestamp", "row_id"])

last = d.groupby("user_id").tail(1)["event"].value_counts()
print("Last page seen on day 0 (trigger population, n=%d)" % len(pop))
print((last.head(8)).to_string())
print("\nShare of population:")
print((100 * last.head(8) / len(pop)).round(1).to_string())

money = {"wallet_deposit", "payment_selection", "wallet_deposit_success", "wallet_deposit_fail"}
reached_money = set(d.loc[d.event.isin(money), "user_id"])
print("\nviewed a deposit-flow page on day 0:", len(reached_money), f"({100 * len(reached_money) / len(pop):.1f}%)")
print("deposit success on day 0:", d.loc[d.event == "wallet_deposit_success", "user_id"].nunique())