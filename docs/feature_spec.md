# Feature spec: 72-hour return reminder (with measurement)

**Status:** proposal for an A/B test | **Owner:** Kowshik | 

## Problem
Most new users go quiet early. In the public e-wallet data (26,618 registration-intent users), 60-72% of users are at-risk by week 1 and only 4.3-4.7% of those return the following week. Among 13,377 users who did something after the registration form on day 0 and then went silent for days 1-2, 10.18% make an engaged return (2+ page views) on days 3-9.

## Goal and non-goals
- Goal: test whether one well-timed reminder raises the share of quiet users who return in the next 7 days.
- Non-goals: redesigning the payment step (cause unknown), incentives or offers, multi-message sequences, personalisation beyond the resume link.

## Users
Newly registered users who did something beyond the registration form on day 0 and had no activity on days 1-2.

## User stories and acceptance criteria
1. As a new user who started and stopped, I want one reminder that takes me back to where I stopped, so I can continue without searching.
   - Sent once, at 72 hours after entry, only to eligible users in the treatment group.
   - The link opens the last page I saw, or the home screen if that page is unavailable.
2. As a user who had trouble signing in, I want a help link in the reminder, so I can recover access.
   - The message includes a sign-in help link (login was the most common last page, 17.1%).
3. As any user, I want to opt out of reminders in one tap, so I stay in control.
   - The message contains an opt-out; opting out stops all reminders and is logged.
4. As an analyst, I want each eligible user randomly assigned 50/50 and the assignment logged, so results can be analysed by intention to treat.
   - Assignment is recorded at the 72-hour mark for both arms, including users who receive nothing.
5. As an analyst, I want true signup and deposit-failure events, so I stop inferring them from page views.
   - `Registration Submitted` fires when the form is successfully submitted.
   - `Deposit Failed` carries a `failure_reason` (for example declined vs timeout).
6. As an engineer or QA, I want the tracking verified before launch, so the test data can be trusted.
   - No duplicate events (the public data had 2.28% duplicates, mostly pairs on landing, login and registration).
   - The same `user_id` is kept when an email link is opened on another device (66% of email-confirming users in the public data had no earlier verification-page view, probably an ID split).

## Requirements
- Eligibility at 72 hours: a non-registration event on day 0, none on days 1-2.
- Frequency cap: at most one reminder per user in the first 14 days. [Proposal; confirm with product]
- Quiet hours, channel and copy approval: [NEEDED from product and compliance]
- Control group receives no message.

## New events (names follow the tracking plan convention)
`Registration Submitted`, `Deposit Failed` (property `failure_reason`), `Reminder Assigned` (property `arm`), `Reminder Sent`, `Reminder Opened`, `Reminder Clicked`, `Reminder Opted Out`.

## Success metrics
- Primary: 2+ non-registration page views on days 3-9. Baseline 10.18%; needs 3,897 users per arm for a +2 point lift (about 7 weeks at the public data's traffic).
- Secondary: any page view on days 3-9 (13.49%); reached `main` (6.41%).
- Guardrails: opt-out and complaint rates [METRIC NEEDED: no baseline in this data].

## Rollout
50/50 A/B test, fixed horizon, no early stopping on significance, stop early only for a guardrail breach. Decision rule: ship if the primary lift is at least +2 points, the 95% interval excludes zero, and guardrails hold.

## Risks and open questions
- Baseline is observational; a reminder may not change behaviour.
- Message consent rules and channel availability: [NEEDED].
- Users stuck at sign-in may react badly to a generic reminder, hence the help link and the opt-out guardrail.
- Does the app already send lifecycle messages that would overlap? [NEEDED]