import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
fl = pd.read_csv("data/processed/user_flags.csv", index_col="user_id")
co = co.join(fl["heavy_user"])
end = ev["timestamp"].max()


def summarize(users, strict=False):
    m = ev.merge(users[["entry_ts"]], left_on="user_id", right_index=True)
    m = m[m.timestamp > m.entry_ts]
    if strict:                                   # ignore registration-form views as "activity"
        m = m[m.event != "registration"]
    m["week"] = ((m.timestamp - m.entry_ts) // pd.Timedelta(days=7)).astype(int)
    act = {k: set(m.loc[m.week == k, "user_id"]) for k in range(5)}

    def elig(k):
        return users.index[users.entry_ts + pd.Timedelta(days=7 * (k + 1)) <= end]

    e1, e2, e4 = elig(1), elig(2), elig(4)
    a0, a1 = set(e1) & act[0], set(e1) & act[1]
    at_risk = set(e2) & act[0] - act[1]
    return {
        "users": len(users),
        "ret_w1_%": round(100 * len(a1) / len(e1), 1),
        "ret_w4_%": round(100 * len(set(e4) & act[4]) / len(e4), 1),
        "w1_active_%": round(100 * len(a0 & a1) / len(e1), 1),
        "w1_at_risk_%": round(100 * len((a0 - a1)) / len(e1), 1),
        "w1_dormant_%": round(100 * (len(e1) - len(a0 | a1)) / len(e1), 1),
        "at_risk_return_%": round(100 * len(at_risk & act[2]) / len(at_risk), 1),
    }


rows = {
    "baseline": summarize(co),
    "excl_heavy": summarize(co[~co.heavy_user.astype(bool)]),
    "strict_activity": summarize(co, strict=True),
}
print(pd.DataFrame(rows).T.to_string())