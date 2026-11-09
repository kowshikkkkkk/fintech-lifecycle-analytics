# Product metrics (public e-wallet data, Jan-Apr 2021, modified by publisher)

| Metric | Definition | Result | Script |
|---|---|---|---|
| Conversion | Registration-page viewers (24,921, full 7-day window) who reach a deposit-success page within 7 days | 2.7%; 44.0% reach the app | 11_funnel.py |
| Retention | Share of registration-intent users with any event in relative week k | Week 1: 10.0-10.5%; week 4: 4.3-4.9%; week 8: 3.2% | 20_retention.py, 22_sensitivity.py |
| Churn (weekly) | Share of users active in week t-1 not active in week t | App users 77.5% (75.9-79.1%); all users 88.6% | 26_product_metrics.py |
| DAU/MAU | Daily active users / users active in trailing 30 days | App users 5.8%; all users 4.2% | 26_product_metrics.py |
| Engagement | Sessions (30-min gap) per active user per day; pages per session | 1.24 sessions per user per day; median 1 page, mean 4.1; 21.7% of sessions have 5+ pages | 26_product_metrics.py |
| Lifecycle | New / active / resurrected / at-risk / dormant by relative week | Week 1: 10.0% active, 60-72% at-risk | 21_lifecycle.py |

Limits: page views are not completed actions; page grouping and the session rule are assumptions (A15, A16); results describe this sample and are not benchmarks.