# Decision memo: where to act on new-user drop-off

**To:** Product lead, wallet app | **From:** Kowshik |
**Decision requested:** approve (1) a 72-hour return-nudge A/B test and (2) two tracking additions before any redesign work.

## Recommendation
Run a randomized test of a single reminder sent at 72 hours to users who engaged beyond the registration form on day 0 and were silent on days 1-2. In parallel, add event tracking for registration submission and deposit failure reasons. Do not redesign the payment step yet: the data cannot say why users leave it.

## What the data shows
Source: public e-wallet clickstream, 2,555,613 page-view events, 338,828 users, Jan-Apr 2021 (dates and IDs altered by the publisher). Cohort: 26,618 users who viewed the registration page.
- **Funnel (7-day window, 24,921 users):** 44.0% reach the app; 2.7% reach a deposit-success page (680 users). Of 2,348 users who reach payment selection after earlier steps, 72% do not reach success.
- **Retention:** 10.0-10.5% return in week 1, 4.3-4.9% in week 4, 3.2% in week 8.
- **Lifecycle:** in week 1, 60-72% of users are at-risk (active in week 0, silent in week 1) depending on whether registration-form reloads count; of at-risk users, only 4.3-4.7% return the following week.
- **Early behaviour:** reaching a deposit-success page in the first day is the action most associated with week-2 return (+11.9 points after controlling for early activity; 444 users, so imprecise). This is an association, not a cause.

## Options considered
| Option | Why not first |
|---|---|
| Redesign the payment step | 72% loss, but only ~180 users a week and no error data: the cause (price, trust, gateway failure) is unknown |
| Fix registration-to-app drop | Registration-page views are not intent (L1), so the loss may include non-prospects |
| **72-hour nudge test (recommended)** | Large population (13,377 eligible), cheap, measurable, narrow window supported by the lifecycle data |

## The test
Eligible users: 13,377 in the data; baseline return on days 3-9 is 13.49%. To detect +2 points (80% power, alpha 0.05) we need 4,861 users per arm, about 9 weeks at this data's traffic. Guardrail: message opt-out rate [METRIC NEEDED: no baseline here]. Fixed horizon, no early stopping on significance.

## Risks and limits
- Evidence is observational; the nudge's effect is unknown until tested.
- Data are page views, not completed actions; deposit failures have no reason code; one person may appear as several IDs.
- Traffic used for the duration estimate is a proxy for the real app.
- A nudge may annoy users: hence the opt-out guardrail and a pre-set threshold.

## Next steps
1. Approve test and guardrail thresholds. 2. Engineering: add registration-submit and deposit-failure-reason events. 3. Decide channel and message copy.