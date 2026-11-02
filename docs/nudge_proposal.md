# Nudge proposal: 72-hour return reminder

## Target users
Users who viewed the registration page, did something beyond the form in their first 24 hours, and then had no activity on days 1-2. In the public data: 13,377 users (about 1,089 per week).

## Why them (evidence, observational)
- In week 1, 60-72% of users are at-risk (active in week 0, silent in week 1); only 4.3-4.7% of at-risk users return the next week, so the window to act is early.
- These users' baseline engaged return (2+ page views on days 3-9) is 10.18%.
- They went quiet from many pages (most common last page: `login`, 17.1%; no page above 17%).

## Message (draft, untested)
- Channel: [CHANNEL NEEDED: depends on opt-in and availability]
- Principles: one clear action, no assumption about what the user did, no false urgency, no incentive assumed, easy opt-out, a "trouble signing in?" help link because login is the most common last page.
- Draft A: "Pick up where you left off. Tap to continue."
- Draft B: "Need a hand getting started? We're here to help." (link to help)
- This test compares one message against no message; copy variants would be a follow-up test.

## Metrics
- Primary: share with 2+ non-registration page views on days 3-9. Baseline 10.18%.
- Secondary: any page view days 3-9 (13.49%); reached `main` (6.41%); deposit success (0.61%, descriptive only).
- Guardrails: opt-out rate and complaint rate [METRIC NEEDED: no baseline in this data]; observed proxies: `support` visits (0.40%), `profile_recovery` visits (1.58%).

## A/B plan
- Randomize 50/50 at the user level at the 72-hour mark; control receives nothing; analyze by intention-to-treat.
- Stratify by whether the user viewed a deposit-flow page on day 0 (23.8% did); report this one subgroup, no others.
- Size: +2 point MDE needs 3,897 users per arm (7,794 total), about 7 weeks at this data's traffic.
- Stopping rule: fixed horizon, at least two full weeks, no stopping on interim significance; check sample ratio before reading results; stop early only if a guardrail threshold is breached.
- Decision rule: ship if the primary lift is at least +2 points, the 95% interval excludes zero, and guardrails stay within pre-set thresholds.

## Risks and limits
Baseline is observational; page views, not actions; message copy and channel are untested and unavailable in this data; users stuck at login may react badly to a generic reminder.