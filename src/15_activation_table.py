import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
fl = pd.read_csv("data/processed/user_flags.csv", index_col="user_id")

end = ev["timestamp"].max()
co = co[co.entry_ts <= end - pd.Timedelta(days=15)].join(fl["heavy_user"])

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m["day"] = (m.timestamp - m.entry_ts) / pd.Timedelta(days=1)

early = m[(m.day >= 0) & (m.day < 1)]
actions = ["main", "open_account_main", "wallet", "wallet_deposit",
           "wallet_deposit_success", "profile"]

tbl = pd.DataFrame(index=co.index)
for a in actions:
    tbl["did_" + a] = tbl.index.isin(early.loc[early.event == a, "user_id"])

g = early.groupby("user_id")["event"]
tbl["early_events"] = g.size().reindex(tbl.index).fillna(0).astype(int)
tbl["early_pages"] = g.nunique().reindex(tbl.index).fillna(0).astype(int)
tbl["ret_d1_7"] = tbl.index.isin(m.loc[(m.day >= 1) & (m.day < 7), "user_id"])
tbl["ret_d7_14"] = tbl.index.isin(m.loc[(m.day >= 7) & (m.day < 14), "user_id"])
tbl = tbl.join(co["heavy_user"])

print("users:", len(tbl))
print(tbl.drop(columns=["early_events", "early_pages"]).sum())
tbl.to_csv("data/processed/activation.csv")