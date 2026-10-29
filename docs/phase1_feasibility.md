# Phase 1: Data audit and feasibility

## Source
Retentioneering e-wallet dataset. Licence stated on the (archived 3.x) docs page: CC BY-NC-SA 4.0.
Raw and sampled data are not redistributed; code and aggregate results only.

## Verified (observed from the data)
- 2,555,613 rows; 338,828 users; 2021-01-01 to 2021-04-07; no null IDs, events or timestamps; all timestamps parse.
- 58,381 exact duplicate rows (2.28%), mostly pairs, concentrated in landing/login/registration; removed (F1).
- Median events per user = 1; top 0.1% of users (338) = 12.0% of events; flagged `heavy_user`, kept (A6).
- Sequence gaps: 66.1% of `email_confirmed` users lack a prior `verify_email`; 18.5% of `main` users lack a prior login/registration/open_account_main; ~9% of `wallet_deposit_success` users lack a prior `payment_selection` (F2).

## Not possible with this data
- Device, channel, category or amount segmentation (no such fields).
- Observing registration submission, transfer or withdrawal completion.
- Verifying timezone, day-of-week or hour-of-day (dates modified by publisher).
- Separating deposit-failure causes.

## Decisions
A2 meaningful transaction = first `wallet_deposit_success`; A3 cohort = first `registration` view (registration-intent); A5 tie-break by file order; A6 flag heavy users; A7 funnels = "reached page", strict order as lower bound.

## Open items
- Mixpanel: ~2.5M events after dedup exceeds the 1M monthly free cap; sample users, and test-import ~100 events first (timestamps are from 2021).
- Screenshot the licence page for the repo.

## Verdict
Proceed to Phase 2 with reduced scope: no device/category split; segment by entry page and cohort cleanliness instead.