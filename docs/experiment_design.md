# Experiment design: 72-hour return nudge

## Evidence (observational)
- Week 1: 60 to 72% of users are at-risk (did something in week 0, nothing in week 1); of at-risk users only 4.3% return in week 2.
- Users active on days 1-2 return on days 3-9 at 46.9% vs 13.5% for quiet users (association only).

## Hypothesis
A single reminder at 72 hours to users who engaged beyond the registration form in their first 24 hours but were silent on days 1-2 will raise the share who return on days 3-9.

## Design
- Unit: user. Eligibility at 72h: a non-registration event in day 0, none on days 1-2. Randomize 50/50: treatment gets one message, control gets none.
- Channel and message copy: [METRIC NEEDED: channel availability and opt-in rules]
- Analysis: intention-to-treat (everyone assigned, whether or not the message was delivered or opened).

## Metrics
- Primary: share with 2+ non-registration page views on days 3-9 (requires more than a single link landing). Baseline 10.18% (n=13,377 in observed data).
- Secondary: any non-registration page view on days 3-9 (13.49%); reached `main` (6.41%); wallet_deposit_success (0.61%, descriptive only).
- Guardrails: message opt-out and complaint rates [METRIC NEEDED: no baseline in this data]. Observed proxies only: `support` page visits (0.40%), `profile_recovery` visits (1.58%).

## Sample size and duration
- MDE +2 points (10.18% to 12.18%), alpha 0.05 two-sided, power 80%: 3,897 per arm (7,794 total); about 7 weeks at the dataset's traffic (about 1,089 eligible users per week).

## Stopping rule
- Fixed horizon: stop when both arms reach the planned size and at least two full weeks have run. No stopping on interim p-values.
- Stop early only if a guardrail threshold is breached.
- Check the split for sample ratio mismatch before reading results.

## Decision rule
Ship if the primary lift is at least +2 points, the 95% interval excludes zero, and guardrails stay within their thresholds. Otherwise do not ship.

## Limits
Baseline is observational; page views, not actions; novelty effects possible; delivery data unavailable here; this is a design, not a test that was run.