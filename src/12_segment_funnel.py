import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
co = co[co.full_window]

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp >= m.entry_ts) & (m.timestamp <= m.entry_ts + pd.Timedelta(days=7))]
reached = {s: set(m.loc[m.event == s, "user_id"]) for s in
           ["main", "wallet_deposit", "payment_selection", "wallet_deposit_success"]}

groups = {
    "all": co,
    "registration_first": co[co.registration_first],
    "login_before": co[co.login_before],
    "neither": co[~co.registration_first & ~co.login_before],
}

rows = []
for name, g in groups.items():
    ids = set(g.index)
    main_ = ids & reached["main"]
    dep = main_ & reached["wallet_deposit"]
    pay = dep & reached["payment_selection"]
    suc = pay & reached["wallet_deposit_success"]
    rows.append({
        "group": name, "users": len(ids), "main": len(main_),
        "main_to_deposit_pct": round(100 * len(dep) / len(main_), 1),
        "pay_to_success_pct": round(100 * len(suc) / len(pay), 1) if pay else None,
    })
print(pd.DataFrame(rows).to_string(index=False))