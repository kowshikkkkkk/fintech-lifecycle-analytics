import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
end = ev["timestamp"].max()

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[m.timestamp > m.entry_ts]                      # activity = any event after the entry second
m["week"] = ((m.timestamp - m.entry_ts) // pd.Timedelta(days=7)).astype(int)
active = m.groupby(["user_id", "week"]).size().rename("n").reset_index()

# 1) Pooled retention by relative week, using only users whose whole week is observable
rows = []
for k in range(0, 9):
    elig = co[co.entry_ts + pd.Timedelta(days=7 * (k + 1)) <= end]
    act = set(active.loc[active.week == k, "user_id"]) & set(elig.index)
    rows.append({"rel_week": k, "eligible": len(elig), "active": len(act),
                 "retention_pct": round(100 * len(act) / len(elig), 1)})
print(pd.DataFrame(rows).to_string(index=False))

# 2) Cohort table: entry week (Monday start) by relative week
co["entry_week"] = (co.entry_ts.dt.normalize() - pd.to_timedelta(co.entry_ts.dt.day_of_week, unit="D")).dt.date
sizes = co.groupby("entry_week").size().rename("users")
table = {}
for k in range(0, 5):
    col = {}
    for wk, g in co.groupby("entry_week"):
        elig = g[g.entry_ts + pd.Timedelta(days=7 * (k + 1)) <= end]
        if len(elig) < 100:
            continue
        act = set(active.loc[active.week == k, "user_id"]) & set(elig.index)
        col[wk] = round(100 * len(act) / len(elig), 1)
    table[f"W{k}"] = col
out = pd.DataFrame(table).join(sizes, how="right")[["users"] + [f"W{k}" for k in range(5)]]
print("\nRetention % by entry week (blank = fewer than 100 fully observed users)")
print(out.to_string())