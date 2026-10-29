import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
co = co[co.full_window]

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp >= m.entry_ts) & (m.timestamp <= m.entry_ts + pd.Timedelta(days=7))]

steps = ["registration", "main",
         "wallet_deposit", "payment_selection", "wallet_deposit_success"]
reached = {s: set(m.loc[m.event == s, "user_id"]) for s in steps}

cum = set(co.index)
prev_cum = None
rows = []
for s in steps:
    cum &= reached[s] if s != "registration" else cum
    n_page = len(reached[s]) if s != "registration" else len(co)
    rows.append({
        "step": s,
        "reached_page": n_page,
        "pct_cohort": round(100 * n_page / len(co), 1),
        "reached_all_earlier": len(cum),
        "pct_cohort_cum": round(100 * len(cum) / len(co), 1),
        "step_conv_cum": None if prev_cum is None else round(100 * len(cum) / prev_cum, 1),
    })
    prev_cum = len(cum)
print(len(co))
print(pd.DataFrame(rows).to_string(index=False))
