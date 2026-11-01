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
- Primary: share with any non-registration page view on days 3-9. Baseline 13.49% (n=13,377 in observed data).
- Secondary (descriptive, underpowered): wallet_deposit_success on days 3-9. Baseline 0.61%.
- Guardrails: message opt-out / unsubscribe rate [METRIC NEEDED: no baseline in this data]; complaint rate [METRIC NEEDED]. Thresholds set before launch.

## Sample size and duration
- MDE +2 points (13.5% to 15.5%), alpha 0.05 two-sided, power 80%: 4,861 per arm (9,722 total). At the dataset's traffic (about 1,089 eligible users per week) about 9 weeks; a real deployment would use real traffic. +3 points: 2,221 per arm (about 4 weeks). +1 point: impractical (about 35 weeks).

## Stopping rule
- Fixed horizon: stop when both arms reach the planned size and at least two full weeks have run. No stopping on interim p-values.
- Stop early only if a guardrail threshold is breached.
- Check the split for sample ratio mismatch before reading results.

## Decision rule
Ship if the primary lift is at least +2 points, the 95% interval excludes zero, and guardrails stay within their thresholds. Otherwise do not ship.

## Limits
Baseline is observational; page views, not actions; novelty effects possible; delivery data unavailable here; this is a design, not a test that was run.