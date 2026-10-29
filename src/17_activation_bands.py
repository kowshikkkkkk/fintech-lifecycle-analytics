import pandas as pd

t = pd.read_csv("data/processed/activation.csv", index_col="user_id")
t = t[t.early_events >= 2].copy()  # users with only the registration view cannot have done another action
t["band"] = pd.cut(t.early_events, bins=[1, 2, 4, 9, 10**6], labels=["2", "3-4", "5-9", "10+"])
actions = [c for c in t.columns if c.startswith("did_")]
outcome = "ret_d7_14"
MIN_N = 30

print("users with 2+ early events:", len(t))
print(t.band.value_counts().sort_index().to_string(), "\n")

diffs, weights = {}, {}
for a in actions:
    name = a.replace("did_", "")
    diffs[name], weights[name] = {}, {}
    for b, g in t.groupby("band", observed=True):
        yes, no = g[g[a]], g[~g[a]]
        if len(yes) < MIN_N or len(no) < MIN_N:
            continue
        diffs[name][b] = 100 * (yes[outcome].mean() - no[outcome].mean())
        weights[name][b] = len(g)

out = pd.DataFrame(diffs).T.round(1)
pooled = {n: round(sum(diffs[n][b] * weights[n][b] for b in diffs[n]) / sum(weights[n].values()), 1)
          for n in diffs if diffs[n]}
out["pooled_within_band"] = pd.Series(pooled)
print("Difference in week-2 return (pp), did vs did not, within early-activity bands")
print(out.to_string())
print("\n('NaN' = fewer than", MIN_N, "users in the did or did-not group for that band)")