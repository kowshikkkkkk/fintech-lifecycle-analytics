import json
import os
import sys
import time

import pandas as pd
import requests

TOKEN = os.environ["MP_PROJECT_TOKEN"]
HOST = os.environ.get("MP_HOST", "api.mixpanel.com")
SHIFT = pd.Timedelta(days=2002)          # see assumption A9
BATCH = 2000                              # Mixpanel accepts up to 2000 events per request
MAX_BATCHES = int(os.environ.get("MAX_BATCHES", "0")) or None

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", index_col="user_id")
fl = pd.read_csv("data/processed/user_flags.csv", index_col="user_id")

ev = ev[ev.user_id.isin(co.index)].sort_values(["timestamp", "row_id"]).copy()
ev["epoch"] = ((ev.timestamp + SHIFT) - pd.Timestamp("1970-01-01")) // pd.Timedelta(seconds=1)

group = pd.Series("other", index=co.index)
group[co.registration_first] = "registration_first"
group[co.login_before] = "login_before"
ev["entry_group"] = ev.user_id.map(group)
ev["heavy_user"] = ev.user_id.map(fl.heavy_user)

records = [
    {"event": "Page Viewed",
     "properties": {"time": int(t), "distinct_id": u, "$insert_id": f"r{r}",
                    "page_name": p, "entry_group": g, "heavy_user": bool(h)}}
    for t, u, r, p, g, h in zip(ev.epoch, ev.user_id, ev.row_id, ev.event, ev.entry_group, ev.heavy_user)
]
batches = [records[i:i + BATCH] for i in range(0, len(records), BATCH)]
print("users:", ev.user_id.nunique(), "events:", len(records), "batches:", len(batches))
print(ev.drop_duplicates("user_id").entry_group.value_counts().to_string())

if MAX_BATCHES:
    batches = batches[:MAX_BATCHES]
    print("limited to", len(batches), "batches")

session = requests.Session()
imported = 0
for i, b in enumerate(batches, 1):
    resp = session.post(f"https://{HOST}/import", params={"strict": 1}, auth=(TOKEN, ""),
                        headers={"Content-Type": "application/json"}, data=json.dumps(b), timeout=120)
    if resp.status_code != 200:
        print("FAILED at batch", i, resp.status_code, resp.text[:600])
        sys.exit(1)
    imported += resp.json().get("num_records_imported", 0)
    if i % 10 == 0 or i == len(batches):
        print(f"batch {i}/{len(batches)}  imported so far: {imported}")
    time.sleep(0.2)
print("done. imported:", imported)