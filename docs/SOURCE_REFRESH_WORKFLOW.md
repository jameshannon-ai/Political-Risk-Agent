# Source Refresh Workflow

Use saved showcase files for dashboard presentation by default. The dashboard should read from `showcase/` artefacts and should not call Tavily or spend live-search credits unless a task explicitly requests a live refresh.

## When To Refresh

Use a targeted refresh only when a core source requirement is weak enough to affect the credibility of a recommendation. Examples:

- an official policy or regulatory anchor is missing or stale
- a live event trigger has materially changed
- a market/pricing signal is too weak for the decision being shown
- a contrary or easing source is needed to avoid one-way escalation
- source role classification is materially wrong

Do not broad-rerun Tavily just to make a showcase look fresher. If a weakness can be handled by a clearer caveat, source quality note or dashboard presentation, prefer that offline fix.

## Refresh Discipline

Before spending credits, document:

- which source requirement is weak
- why the current source is insufficient
- the exact targeted query or source target
- how the new evidence would change the brief, source audit or confidence score

After a refresh:

- preserve the previous source audit trail where useful
- update selected/rejected source reasoning
- update evidence claims, caveats and refresh triggers
- keep confidence capped if company-specific data is still missing
- rerun `python3 -m unittest discover tests`
- rerun `python3 scripts/quality_check.py`

The goal is better decision evidence, not more sources for their own sake.
