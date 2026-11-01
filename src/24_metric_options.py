import math

import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
end = ev["timestamp"].max()
co = co[co.entry_ts + pd.Timedelta(days=10) <= end]

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp > m.entry_ts) & (m.event != "registration")]
m["day"] = ((m.timestamp - m.entry_ts) // pd.Timedelta(days=1)).astype(int)

day0 = set(m.loc[m.day == 0, "user_id"])
day12 = set(m.loc[m.day.isin([1, 2]), "user_id"])
pop = day0 - day12
n = len(pop)

w = m[m.day.between(3, 9) & m.user_id.isin(pop)]
events_per_user = w.groupby("user_id").size().reindex(list(pop)).fillna(0)


def n_per_arm(p, d, z_a=1.96, z_b=0.8416):
    q = p + d
    pb = (p + q) / 2
    num = z_a * math.sqrt(2 * pb * (1 - pb)) + z_b * math.sqrt(p * (1 - p) + q * (1 - q))
    return math.ceil(num ** 2 / d ** 2)


print("trigger population:", n)
print("\nCandidate primary metrics (days 3-9)")
for name, mask in [("any event (1+)", events_per_user >= 1),
                   ("2+ events", events_per_user >= 2),
                   ("3+ events", events_per_user >= 3)]:
    p = mask.mean()
    print(f"{name:16s} users={int(mask.sum()):5d}  rate={100 * p:5.2f}%  n per arm for +2 pp={n_per_arm(p, 0.02)}")

main = set(w.loc[w.event == "main", "user_id"])
print(f"\nreached main:      users={len(main)}  rate={100 * len(main) / n:.2f}%")

print("\nProxy guardrails (NOT opt-out or complaint rates)")
for page in ["support", "profile_recovery"]:
    u = set(w.loc[w.event == page, "user_id"])
    print(f"{page:17s} users={len(u):4d}  rate={100 * len(u) / n:.2f}%")