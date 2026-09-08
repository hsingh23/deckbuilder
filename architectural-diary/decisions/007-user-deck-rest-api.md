# ADR 007 — REST user-deck endpoints as a first-class API

- **Date:** 2014-04-29 – 2014-04-30 (7fcd595, 57a9379, 551e8c8, ec32887)
- **Status:** accepted, but shipped as a draft (known bugs, see AGENTS.md)

## Context

Once users can log in (ADR 006), the product story is "save my merged deck". The team
also wanted the door open for non-browser clients, so deck storage was exposed as JSON
HTTP endpoints rather than as server-rendered pages.

## Decision

`app/userdeck_views.py` provides CRUD under `/user/`: `GET /user/<google_id>` lists a
user's decks, `POST /user/` inserts, `PUT /user/` updates by `deck_id`, `DELETE
/user/<deck_id>` removes — all returning JSON, backed by the `UserDecks` table
(`google_id` FK, raw deck JSON, optional latitude/longitude for a moot geo feature).
A `jsonp` decorator in `utils.py` was added for cross-domain reads. The frontend gained
the matching "save to my decks / append / export to Quizlet" button template.

## Consequences

- The API is discoverable and could serve a mobile client unchanged.
- It was committed rough: the GET query string is malformed (`WHERE google_id` with no
  `= %s`, argument not a tuple), POST/PUT read from the query string instead of the
  body, and a bare `except` returns `{"error": ...}` for everything — the buttons in the
  UI template are not wired to these routes yet.
- No authorization: any caller knowing a `google_id` can read or delete that user's
  decks. Fine for a demo; not fine in production.
