import json
import os

import pandas as pd
import requests

TOKEN = os.environ["MP_PROJECT_TOKEN"]
HOST = os.environ.get("MP_HOST", "api.mixpanel.com")
SHIFT_DAYS = 2002  # 286 weeks: keeps weekdays, puts data inside Mixpanel's 1825-day window

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"]).head(100)

payload = [
    {
        "event": "Page Viewed",
        "properties": {
            "time": int((r.timestamp + pd.Timedelta(days=SHIFT_DAYS)).tz_localize("UTC").timestamp()),
            "distinct_id": r.user_id,
            "$insert_id": f"r{r.row_id}",
            "page_name": r.event,
        },
    }
    for r in ev.itertuples()
]

print("first event:", json.dumps(payload[0]))
print("events in this batch:", len(payload))

resp = requests.post(
    f"https://{HOST}/import",
    params={"strict": 1},
    auth=(TOKEN, ""),
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload),
    timeout=60,
)
print(resp.status_code, resp.text)