import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
end = ev["timestamp"].max()
K = 8

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[m.timestamp > m.entry_ts]                      # activity = any event after the entry second
m["week"] = ((m.timestamp - m.entry_ts) // pd.Timedelta(days=7)).astype(int)
w = m[m.week <= K].groupby(["user_id", "week"]).size().reset_index()

act = pd.DataFrame(False, index=co.index, columns=range(K + 1))
for k in range(K + 1):
    act.loc[w.loc[w.week == k, "user_id"], k] = True


def states(k):
    """Lifecycle state of each user in relative week k (only users whose week k is fully observed)."""
    elig = co.entry_ts + pd.Timedelta(days=7 * (k + 1)) <= end
    a, p = act[k], act[k - 1]
    s = pd.Series("", index=co.index)
    s[a & p] = "active"
    s[a & ~p] = "resurrected"
    s[~a & p] = "at_risk"
    s[~a & ~p] = "dormant"
    return s[elig]


order = ["active", "resurrected", "at_risk", "dormant"]
rows = []
for k in range(1, K + 1):
    s = states(k)
    row = {"rel_week": k, "eligible": len(s)}
    for name in order:
        row[name + "_%"] = round(100 * (s == name).mean(), 1)
    rows.append(row)
print("Lifecycle state shares by relative week (week 0 = New for every user)")
print(pd.DataFrame(rows).to_string(index=False))

s1, s2 = states(1), states(2)
both = s1.index.intersection(s2.index)
print("\nState in week 1 (rows) versus week 2 (columns), counts, users eligible for week 2:", len(both))
print(pd.crosstab(s1[both], s2[both]).reindex(index=order, columns=order, fill_value=0).to_string())