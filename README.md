# Fintech Product Lifecycle Analytics

Analysis of onboarding, activation and retention for a digital-wallet app, using the public Retentioneering e-wallet clickstream dataset.

**Status:** work in progress. Data audit, funnel and activation analysis are complete; Mixpanel reports, retention and lifecycle states, experiment design and the decision memo are in progress.

## Data
Retentioneering e-wallet dataset: 2,555,613 events, 338,828 users, Jan to Apr 2021 (dates and IDs modified by the publisher). Licence stated on the source page: CC BY-NC-SA 4.0. The data is not included in this repository; download it from the source and place it at `data/raw/e_wallet.csv`.

## What's here
- `src/`: numbered scripts (audit, cleaning, cohort, funnel, activation, Mixpanel import)
- `docs/`: assumptions log, fix log, findings, limits, Phase 1 feasibility report

## Findings so far (observed; associations, not causal)
- 58,381 exact duplicate events (2.28%) removed and logged.
- In a 7-day funnel for 24,921 registration-intent users, 2.7% reached a deposit-success page; 72.2% of users at payment selection did not reach one.
- After holding first-day activity roughly constant, reaching deposit success is the early action most associated with week-2 return (+11.9 pp, small group).
- Limits: the data are page views, not completed actions; see `docs/readme_limits.md`.