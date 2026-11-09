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
| A12 | Assumption | Retention and lifecycle use weeks relative to each user's own entry; "active" = any event after the entry second; a week counts only if fully observed; states: new (week 0), active, resurrected, at-risk, dormant per the rule table in docs/retention_design.md | Short user lifespans (median 1 event) make weekly thresholds coarse but standard; right-censoring handled by eligibility |
| A13 | Assumption | Experiment design uses this dataset's traffic (about 1,089 eligible users per week) as a proxy for real traffic; MDE +2 points; two-sided alpha 0.05; 80% power | A real deployment would set duration from its own volume |
| A14 | Assumption | Primary experiment metric is 2+ non-registration page views on days 3-9, to avoid counting a single message-click landing as a return; "any event" and "reached main" are secondary | Treatment could mechanically create 1-page-view returns; guardrail proxies (support, profile_recovery) are not opt-out rates |
| A15 | Assumption | "App users" = users with an event on an in-app or money page (list in src/26_product_metrics.py); page grouping is my reading of page names | Source documentation gives no page hierarchy |
| A16 | Assumption | A session ends after 30 minutes without an event; no session IDs exist in the data | Standard convention; timestamps have second granularity |