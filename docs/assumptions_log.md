# Assumptions log
Observed = computed from the data. Assumption = my decision, not provable from the data.

| ID | Type | Statement | Evidence / reason |
|---|---|---|---|
| A1 | Observed | Rows are page views, not completed actions | Dataset documentation |
| A2 | Assumption | Meaningful transaction = a user's first `wallet_deposit_success`; `wallet_deposit_fail` is tracked separately as friction | Success is the only page confirming money moved; transfer and withdrawal have no success page |
| A3 | Assumption | Cohort = users with at least one `registration` view, entry = first view; called "registration-intent cohort" (26,618 users) | Submission is not observable; sensitivity check on registration-first subset (9,356) and login-before subset (4,779) |
| A4 | Limit | Failure causes (declined vs server timeout) cannot be separated | No error code in the data |