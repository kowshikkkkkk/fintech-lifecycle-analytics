import math
import pandas as pd


def wilson(k, n, z=1.96):
    """95% Wilson confidence interval for a proportion, in percent."""
    if n == 0:
        return None, None
    p = k / n
    d = 1 + z**2 / n
    c = p + z**2 / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return round(100 * (c - h) / d, 1), round(100 * (c + h) / d, 1)


ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
fl = pd.read_csv("data/processed/user_flags.csv", index_col="user_id")
co = co[co.full_window].join(fl["heavy_user"])

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp >= m.entry_ts) & (m.timestamp <= m.entry_ts + pd.Timedelta(days=7))]
steps = ["main", "wallet_deposit", "payment_selection", "wallet_deposit_success"]
reached = {s: set(m.loc[m.event == s, "user_id"]) for s in steps}


def funnel(ids, label):
    cum, prev = set(ids), len(ids)
    for s in steps:
        cum &= reached[s]
        lo, hi = wilson(len(cum), prev)
        print(f"{label:14s} {s:24s} users={len(cum):6d}  "
              f"step_conv={100 * len(cum) / prev:5.1f}%  95% CI [{lo}, {hi}]")
        prev = len(cum)


funnel(co.index, "all")
print()
funnel(co.index[~co.heavy_user.astype(bool)], "excl_heavy")
print("\nheavy users in cohort:", int(co.heavy_user.sum()))