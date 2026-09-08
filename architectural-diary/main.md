# Architectural diary — DeckJam

An index of the design decisions that shaped this codebase, reconstructed from the
rewritten git history (March–April 2014, 45 commits by Harsh Singh and Hilal Habashi).
Each entry links to a decision record with context, the decision, and its consequences.

## Timeline at a glance

| Phase | When | What happened |
|---|---|---|
| Scaffold | Mar 21 – Apr 18 | Flask skeleton with server-rendered keyword form; CoffeeScript/Handlebars UI lands on a dev branch |
| Interactive UI | Apr 18 – 22 | lunr filtering, YUI autocomplete, schema rework to raw-JSON caching, merge to master |
| DB integration | Apr 22 – 27 | `usedb` branch: connection handling, quizlet-backup drafts, working cache pipeline with stored-procedure upsert |
| Deployment | Apr 24 – 25 | EWS CGI attempts → package restructure → DigitalOcean Apache/mod_wsgi |
| Identity & user decks | Apr 26 – 30 | Google OAuth, `google_id` primary key, REST user-deck CRUD, filter/export wiring |

## Decisions

1. [Cache raw Quizlet JSON instead of normalizing into card rows](decisions/001-cache-quizlet-json-not-normalized.md) — the defining schema pivot.
2. [One shared MySQL connection, per-query cursors](decisions/002-single-shared-mysql-connection.md) — fixing the multiple-connection bug class.
3. [From CGI hacks to Apache mod_wsgi on DigitalOcean](decisions/003-cgi-to-wsgi-deployment.md) — the deployment journey.
4. [A client-heavy CoffeeScript frontend behind a thin JSON backend](decisions/004-client-heavy-frontend.md) — why almost all UX logic lives in deckjam.coffee.
5. [Weekly keyword freshness with a stored-procedure upsert](decisions/005-weekly-freshness-upsert.md) — the caching policy.
6. [Google identity via google_id as the Users primary key](decisions/006-google-identity-primary-key.md) — skipping passwords entirely.
7. [REST user-deck endpoints as a first-class API](decisions/007-user-deck-rest-api.md) — saved decks keyed by Google id.
8. [Staying on Python 2 and the Quizlet 2.0 API (archival posture)](decisions/008-python2-quizlet-legacy.md) — what froze, and what a revival needs.

## Reading the history

Commit messages were rewritten messages-only on 2026-09-08 (see the note at the top of
[CHANGELOG.md](../CHANGELOG.md)); every decision record cites post-rewrite hashes.
For the original messages, see local branch `backup/pre-docs-20260908`.
