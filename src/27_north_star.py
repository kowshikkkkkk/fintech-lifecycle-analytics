from collections import Counter

import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
APP = ["main", "account", "account_details", "account_info", "accounts_main", "accounts_kids",
       "profile", "profile_edit", "order_history", "order_statistics", "support", "special_offers",
       "referral_program", "loyalty_program", "subscriptions", "tariff_plans", "wallet",
       "wallet_deposit", "payment_selection", "wallet_deposit_success", "wallet_deposit_fail",
       "wallet_transfer", "wallet_withdrawal"]

ev["date"] = ev.timestamp.dt.normalize()
ev["week"] = ev.date - pd.to_timedelta(ev.date.dt.day_of_week, unit="D")
last = ev.date.max()
weeks = [w for w in sorted(ev.week.unique())
         if w >= pd.Timestamp("2021-01-04") and w + pd.Timedelta(days=6) <= last]   # full Mon-Sun weeks

dep = {w: set(g) for w, g in ev[ev.event == "wallet_deposit_success"].groupby("week").user_id}
app_users = {w: set(g) for w, g in ev[ev.event.isin(APP)].groupby("week").user_id}

rows = []
for w in weeks:
    d = dep.get(w, set())
    rows.append({"week_start": w.date(), "weekly_depositors": len(d),
                 "weekly_app_users": len(app_users[w]),
                 "depositors_pct_of_app_users": round(100 * len(d) / len(app_users[w]), 1)})
t = pd.DataFrame(rows)
print(t.to_string(index=False))
print(f"\nmean weekly depositors {t.weekly_depositors.mean():.0f} "
      f"(min {t.weekly_depositors.min()}, max {t.weekly_depositors.max()})")
print(f"mean share of weekly app users {t.depositors_pct_of_app_users.mean():.1f}% "
      f"(range {t.depositors_pct_of_app_users.min()}% to {t.depositors_pct_of_app_users.max()}%)")

weeks_with_deposit = Counter()
for w in weeks:
    for u in dep.get(w, set()):
        weeks_with_deposit[u] += 1
n = len(weeks_with_deposit)
rep = sum(1 for v in weeks_with_deposit.values() if v >= 2)
print(f"\nusers with a deposit success in any full week: {n}; in 2+ different weeks: {rep} ({100 * rep / n:.1f}%)")