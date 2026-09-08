# ADR 001 — Cache raw Quizlet JSON instead of normalizing into card rows

- **Date:** 2014-04-22 (ce385be), refined 2014-04-26 (e24d849)
- **Status:** accepted, defining decision

## Context

The initial scaffold (e439b4c) shipped a classic normalized schema: `Keyword`, `Deck`,
`Card` tables and a `FullTable` view. Quizlet data would have been shredded into rows on
import and re-joined on read. But the app never queries individual cards server-side —
the frontend wants whole decks (title, term count, terms + definitions) to render and
index in lunr.

## Decision

Rewrite `create.sql` around **raw JSON blobs**: `QuizletDecks(quizlet_id, json)` stores
each Quizlet set exactly as the API returned it; `Keywords` + `KeywordsQuizletDecks`
track which keyword fetched which deck and when. Reads return the stored JSON directly
(`get_decks_from_database` decodes it back to objects). The only SQL-side derived value
is an average (`terms_selected/GREATEST(times_deck_selected,1)`).

## Consequences

- Import logic shrank to a single stored-procedure upsert (see ADR 005); no row mapping
  to maintain when Quizlet's payload shape changed.
- Filtering/selection all moved client-side — reinforcing ADR 004's thin-JSON backend.
- JSON grew to `MEDIUMTEXT` after `TEXT` proved small enough to matter for 50-set
  keyword pulls (0252ff1).
- Any server-side analytics on terms/definitions became impossible without re-parsing
  JSON per row — accepted because the only analytics wanted (search counts) live on the
  keyword/deck counters.
