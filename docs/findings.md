# Findings (observed unless marked)
- Funnel (7-day window, n=24,921): reached `main` 44.0%; reached a deposit success page 2.7% (1.5% strict).
- Segment split: `main` reached by 22.0% of registration-first users vs 61.6% of login-before users.
- Main-to-deposit conversion is similar across groups (35.2% to 38.0%); the "existing users inflate the drop" hypothesis was not supported (not significance-tested).
- [PENDING] Confidence intervals; rerun excluding heavy users (A6); check other app pages as the "reached app" proxy.
- Registration-first users (n=8,698, 7-day window): 22.0% reach `main`; 34.2% reach any app or signup-stage page; 59.6% only ever view `registration`.
- Of those, ~32.5% of the group are single-event bounces; ~2,360 viewed `registration` more than once and nothing else (cause unknown: indecision vs form errors).
- Using `main` alone as "reached the app" overstated the loss by ~12 points.