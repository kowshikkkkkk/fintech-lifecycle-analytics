import math
import pandas as pd

t = pd.read_csv("data/processed/activation.csv", index_col="user_id")
actions = [c for c in t.columns if c.startswith("did_")]


def diff_ci(k1, n1, k0, n0, z=1.96):
    """Difference in proportions (did minus did not), with a 95% interval, in percentage points."""
    p1, p0 = k1 / n1, k0 / n0
    se = math.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    d = p1 - p0
    return 100 * d, 100 * (d - z * se), 100 * (d + z * se)


for outcome in ["ret_d7_14", "ret_d1_7"]:
    rows = []
    for a in actions:
        yes, no = t[t[a]], t[~t[a]]
        d, lo, hi = diff_ci(yes[outcome].sum(), len(yes), no[outcome].sum(), len(no))
        rows.append({
            "action": a.replace("did_", ""),
            "n_did": len(yes),
            "ret_did_%": round(100 * yes[outcome].mean(), 1),
            "n_not": len(no),
            "ret_not_%": round(100 * no[outcome].mean(), 1),
            "diff_pp": round(d, 1),
            "ci_95": f"[{lo:.1f}, {hi:.1f}]",
        })
    print("\nOutcome:", outcome)
    print(pd.DataFrame(rows).to_string(index=False))