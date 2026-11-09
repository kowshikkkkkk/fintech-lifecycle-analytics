import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
APP = ["main", "account", "account_details", "account_info", "accounts_main", "accounts_kids",
       "profile", "profile_edit", "order_history", "order_statistics", "support", "special_offers",
       "referral_program", "loyalty_program", "subscriptions", "tariff_plans", "wallet",
       "wallet_deposit", "payment_selection", "wallet_deposit_success", "wallet_deposit_fail",
       "wallet_transfer", "wallet_withdrawal"]
ev["date"] = ev.timestamp.dt.normalize()
first, last = ev.date.min(), ev.date.max()


def dau_mau(df, label):
    days = pd.date_range(first, last)
    dau = df.groupby("date").user_id.nunique().reindex(days, fill_value=0)
    by_day = {d: set(g) for d, g in df.groupby("date").user_id}
    rows = []
    for d in days[29:]:
        window = set().union(*[by_day.get(x, set()) for x in pd.date_range(d - pd.Timedelta(days=29), d)])
        rows.append({"date": d, "dau": dau[d], "mau": len(window)})
    t = pd.DataFrame(rows)
    t["stickiness"] = t.dau / t.mau
    print(f"\n{label}: {len(t)} days with a full 30-day window")
    print(f"  average DAU {t.dau.mean():,.0f} | average MAU {t.mau.mean():,.0f} | "
          f"DAU/MAU mean {100 * t.stickiness.mean():.1f}% (min {100 * t.stickiness.min():.1f}%, max {100 * t.stickiness.max():.1f}%)")
    return t


dau_mau(ev, "All users (any page)")
dau_mau(ev[ev.event.isin(APP)], "App users (in-app and money pages only)")

# Engagement: sessions with a 30-minute inactivity gap
s = ev.sort_values(["user_id", "timestamp", "row_id"]).copy()
gap = s.groupby("user_id").timestamp.diff()
s["session"] = ((gap.isna()) | (gap > pd.Timedelta(minutes=30))).cumsum()
sess = s.groupby("session").agg(user_id=("user_id", "first"), start=("timestamp", "min"),
                                end=("timestamp", "max"), pages=("event", "size"))
sess["date"] = sess.start.dt.normalize()
daily = sess.groupby(["date", "user_id"]).size()
print("\nEngagement (30-minute session rule)")
print(f"  sessions: {len(sess):,} | mean pages per session {sess.pages.mean():.1f} | median {sess.pages.median():.0f}")
print(f"  sessions per active user per day: {daily.mean():.2f}")
print(f"  share of sessions with 1 page: {100 * (sess.pages == 1).mean():.1f}% | with 5+ pages: {100 * (sess.pages >= 5).mean():.1f}%")

# Weekly churn on full calendar weeks (Mon-Sun)
ev["week"] = ev.date - pd.to_timedelta(ev.date.dt.day_of_week, unit="D")
weeks = sorted(ev.week.unique())
full = [w for w in weeks if w >= pd.Timestamp("2021-01-04") and w + pd.Timedelta(days=6) <= last]
act = {w: set(g) for w, g in ev.groupby("week").user_id}
app_act = {w: set(g) for w, g in ev[ev.event.isin(APP)].groupby("week").user_id}
for label, a in [("All users", act), ("App users", app_act)]:
    ch = [100 * len(a[p] - a[c]) / len(a[p]) for p, c in zip(full[:-1], full[1:])]
    print(f"\nWeekly churn, {label}: weeks {full[0].date()} to {full[-1].date()}: mean {sum(ch) / len(ch):.1f}%, range {min(ch):.1f}% to {max(ch):.1f}%")
    print(f"  average weekly active users: {sum(len(a[w]) for w in full) / len(full):,.0f}")