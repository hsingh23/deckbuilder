# ADR 004 — A client-heavy CoffeeScript frontend behind a thin JSON backend

- **Date:** 2014-04-18 – 2014-04-30 (6e82bec, ce385be, c9704b3, 4cdb34d)
- **Status:** accepted

## Context

Version one was a server-rendered form: type a keyword, POST, reload the page with
results. For a deck-merging tool — where the user iteratively filters, selects, and
exports across many decks — full page reloads would destroy the selection state each
time.

## Decision

Move the entire interaction model into the browser. `deckjam.coffee` (originally
`all.coffee`, 6e82bec) owns: fetching decks, rendering them with a client-side
Handlebars template, indexing them into lunr.js for substring filtering, drag-to-select
card state, and export. Flask shrinks to JSON endpoints (`/decks/<keyword>`,
`/combinations`, `/user/...`) plus one Jinja page that bootstrips the Handlebars
templates and asset bundles. In c9704b3 the frontend stopped calling the Quizlet API
directly and switched to the local `/decks` route, putting the MySQL cache (ADR 001) in
the path of every search.

## Consequences

- Selection/filter state survives across deck fetches; the UX works offline against
  cached decks.
- All state lives in the DOM (`$(".card.selected")`) — no frontend model; Export reads
  the DOM directly. Simple, but impossible to unit-test.
- The server is stateless per request and trivially cacheable; a future mobile client
  could reuse the same JSON API (that's partly what `/user/...` anticipated, ADR 007).
- Handlebars-inside-Jinja required `{% raw %}` blocks; template ownership is split
  between two systems (see AGENTS.md gotchas).
