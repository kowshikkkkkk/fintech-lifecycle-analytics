# Assumptions log
Observed = computed from the data. Assumption = my decision, not provable from the data.

| ID | Type | Statement | Evidence / reason |
|---|---|---|---|
| A1 | Observed | Rows are page views, not completed actions | Dataset documentation |
| A2 | Assumption | Meaningful transaction = a user's first `wallet_deposit_success`; `wallet_deposit_fail` is tracked separately as friction | Success is the only page confirming money moved; transfer and withdrawal have no success page |
| A3 | Assumption | Cohort = users with at least one `registration` view, entry = first view; called "registration-intent cohort" (26,618 users) | Submission is not observable; sensitivity check on registration-first subset (9,356) and login-before subset (4,779) |
| A4 | Limit | Failure causes (declined vs server timeout) cannot be separated | No error code in the data |
| A5 | Assumption | Same-second ties are ordered by original file row (`row_id`) | The timestamp has second granularity; file order is the only available tie-break |
| A6 | Assumption | Users above the 99.9th percentile of event count are flagged `heavy_user` and kept; all event-count results are reported with and without them | Cannot distinguish power users, shared IDs and automation; timing of top 20 users showed no clear bot signature |
| A7 | Assumption | Funnels are reported primarily as "reached page after cohort entry"; strict sequence order is a lower-bound sensitivity check | 66% of `email_confirmed` users lack a prior `verify_email` (likely ID split across devices); strict order would undercount and show an artificial drop-off |
| A8 | Assumption | Mixpanel event model: single `Page Viewed` event with `page_name` property; timestamps treated as UTC; `$insert_id` = `r` + row_id | Source has no timezone or action events; page-view data fits the single-event pattern |