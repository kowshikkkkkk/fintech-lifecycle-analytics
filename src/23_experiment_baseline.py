import math

import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
end = ev["timestamp"].max()
co = co[co.entry_ts + pd.Timedelta(days=10) <= end]     # outcome window (days 3-9) fully observed

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp > m.entry_ts) & (m.event != "registration")]
m["day"] = ((m.timestamp - m.entry_ts) // pd.Timedelta(days=1)).astype(int)

day0 = set(m.loc[m.day == 0, "user_id"])                 # did something beyond the form in the first 24h
day12 = set(m.loc[m.day.isin([1, 2]), "user_id"])        # any activity on days 1-2
back = set(m.loc[m.day.between(3, 9), "user_id"])        # outcome: any activity on days 3-9
dep = set(m.loc[(m.event == "wallet_deposit_success") & m.day.between(3, 9), "user_id"])

pop = day0 - day12                                       # trigger population at the 72-hour mark
base = len(pop & back) / len(pop)


def n_per_arm(p, d, z_a=1.96, z_b=0.8416):               # two-sided alpha 0.05, power 80%
    q = p + d
    pb = (p + q) / 2
    num = z_a * math.sqrt(2 * pb * (1 - pb)) + z_b * math.sqrt(p * (1 - p) + q * (1 - q))
    return math.ceil(num ** 2 / d ** 2)


e = co.loc[list(pop), "entry_ts"]
per_week = len(pop) / ((e.max() - e.min()).days / 7)

print("cohort users with 10+ days observed:", len(co))
print("did something beyond the form in first 24h:", len(day0))
print("trigger population (quiet on days 1-2):", len(pop))
print(f"baseline return on days 3-9: {len(pop & back)} users = {100 * base:.2f}%")
print(f"baseline deposit success on days 3-9: {len(pop & dep)} users = {100 * len(pop & dep) / len(pop):.2f}%")
print(f"users active on days 1-2 who return on days 3-9: {100 * len(day12 & back) / len(day12):.1f}% ({len(day12)} users)")
print(f"arrivals into the trigger population: about {per_week:.0f} per week")
for d in (0.01, 0.02, 0.03):
    n = n_per_arm(base, d)
    print(f"detect +{100 * d:.0f} pp: {n} per arm, {2 * n} total, about {2 * n / per_week:.1f} weeks")