# ADR 005 — Weekly keyword freshness with a stored-procedure upsert

- **Date:** 2014-04-26 (e24d849), repair 2014-04-27 (9977f06)
- **Status:** accepted

## Context

Quizlet search results change slowly. Re-fetching on every request would burn API quota
(the client-id auth had low limits) and add seconds of latency; never re-fetching would
serve stale decks. Early drafts (`quizlet-backup.py`, f2df9dd) sketched this policy in
broken pseudo-code; `quizletdeck.py` was never more than a sketch.

## Decision

`quizlet.get_decks(keyword)` resolves the keyword row first (`get_or_create_keyword`),
then re-queries Quizlet **only if** the row was just created, has no decks linked, or its
`last_updated` is older than **one week** (`expired_keyword`). Refreshes go through the
`create_or_update_quizlet(quizlet_id, keyword_id, json)` MySQL stored procedure, which
inserts or updates the JSON blob atomically, so concurrent refreshes can't duplicate
decks. Every search bumps `Keywords.times_searched` (551e8c8) for the popularity feed
(`cacheagent.get_most_searched_decks`).

## Consequences

- Repeat searches are one SQL join; the API is hit at most weekly per keyword.
- Business logic lives partly in SQL (the procedure) — invisible to Python tests, and
  `create.sql` must be applied for the app to work at all.
- The freshness check originally compared dates with the operator inverted; 9977f06
  fixed it — a reminder that hand-rolled date math needs tests.
- `times_searched`/`terms_selected` counters were wired for an analytics feature that
  never fully shipped (the "most searched decks" endpoint exists but is unrouted).
