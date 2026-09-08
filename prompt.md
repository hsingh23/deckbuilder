# One-shot recreation prompt — DeckJam (deckbuilder)

Paste the prompt below to an AI coding agent to recreate this application from scratch.
It encodes every design decision the original made, so the result should be
functionally identical (modulo era-inevitable library versions).

---

Build "DeckJam", a web app that lets a student search Quizlet for flashcard decks by
keyword, view all matching decks on one page, filter them, multi-select individual
cards, and export the merged selection as JSON, optionally saving it as a personal deck
attached to their Google account.

## Exact stack (2014-faithful)

- **Python 2.7**, **Flask 0.10.1**, simplejson for JSON
- **Flask-OAuth 0.12** for Google OAuth2; session-stored access token
- **MySQL** via **MySQL-python (MySQLdb) 1.2.3** — raw parameterized SQL, no ORM
- **Flask-Assets 0.9 / webassets** with `coffeescript`, `scss`, and `jsmin` filters
- Frontend: **CoffeeScript** compiled to `gen/` bundles; **jQuery 1.11.0**,
  **Handlebars 1.3.0** (runtime + compiler), **lunr.js**, **Underscore.js**,
  **YUI 3.16** (autocomplete only), **Bootstrap 3** (vendored CSS) — all vendored
  locally under `static/`, no CDNs except the YUI loader script
- Serving: Apache 2 + mod_wsgi via `deckbuilder.wsgi`; a `deckbuilder.virtualhost`
  file for the site; a `dev.py` launcher for local development (0.0.0.0:5000, debug)
- Configuration in a **gitignored `app/__config.py`** exposing the names:
  `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `QUIZLET_CLIENT_KEY`, `DATABASE_HOST`,
  `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_DATABASE`. Never commit values.

## Build order

1. **Scaffold** — Flask app factory in `app/__init__.py`; Jinja `base.html` +
   `index.html`; asset bundles: `all_dev_js` (dev libs + coffee, output `gen/dev.js`),
   `all_js` (min libs, jsmin, output `gen/packed.js`), `scss` (output `gen/main.css`).
2. **Database schema** (`create.sql`) — see data model below, plus the stored procedure.
3. **Search cache pipeline** (`app/quizlet.py`) — keyword row → freshness check →
   Quizlet fetch → upsert → read back as JSON.
4. **Frontend** (`app/static/coffee/deckjam.coffee` + `util.coffee`) — fetch, render,
   index, filter, select, export (details below).
5. **Google OAuth** (`app/views.py`) — `/login`, `/oauth2callback`, userinfo fetch.
6. **User decks API** (`app/userdeck_views.py`) + `app/utils.py` JSONP decorator.
7. **Deployment files** — `deckbuilder.wsgi`, `deckbuilder.virtualhost`, `.htaccess`
   relic, `requirements.txt`.

## Data model (MySQL, InnoDB)

- `Users(google_id INT PK, name VARCHAR(1024), picture_url VARCHAR(2083), email VARCHAR(2083), preference TEXT)` — google_id IS the primary key; no passwords anywhere.
- `Keywords(keyword_id INT UNSIGNED PK AUTO_INCREMENT, keyword VARCHAR(1024), last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, times_searched INT UNSIGNED DEFAULT 0)`
- `QuizletDecks(quizlet_id INT UNSIGNED PK, json MEDIUMTEXT)` — raw Quizlet set JSON, never normalized into card rows.
- `UserDecks(deck_id INT PK AUTO_INCREMENT, google_id INT → Users, created_on TIMESTAMP, json MEDIUMTEXT, latitude FLOAT(10,6) NULL, longitude FLOAT(10,6) NULL)`
- `KeywordsQuizletDecks(keyword_id → Keywords, quizlet_id → QuizletDecks, terms_selected INT UNSIGNED DEFAULT 0, times_deck_selected INT UNSIGNED DEFAULT 0)`
- `KeywordsUserDecks(keyword_id → Keywords, deck_id → UserDecks)`
- Stored procedure `create_or_update_quizlet(new_quizlet_id, new_keyword_id, new_json)`:
  INSERT the deck + keyword link if the quizlet_id is absent, else UPDATE the JSON.

## Database access rules

- Exactly ONE shared MySQLdb connection, lazily created and cached on
  `app.config["connection"]` in `app/db.py`. Never open a second connection (a
  DictCursor second connection once caused interleaved-transaction corruption).
- Helpers: `query_one(sql, args)`, `query_all(sql, args)` (open cursor → execute →
  fetch → close cursor), `make_dicts(cursor, rows)` builds dicts from
  `cursor.description` (do NOT use DictCursor). Writes: explicit cursor +
  `cursor.connection.commit()`.

## Backend APIs (all under the Flask app)

- `GET /` and `GET /index` — render `index.html`.
- `GET /decks/<keyword>` — JSON array of cached decks for ONE keyword (flat list, not a
  dict keyed by keyword). Pipeline: get-or-create Keywords row; re-fetch from Quizlet
  only if (a) row just created, (b) no decks linked, or (c) `last_updated` older than 7
  days; refresh = Quizlet `search/sets` (per_page=50, page=1) → `sets?set_ids=...` →
  call `create_or_update_quizlet` per set; then SELECT the join and return JSON, bumping
  `times_searched`.
- `GET|POST /combinations?k=a,b,c` — all ordered keyword combinations from longest to
  shortest, via a custom `combinations()` iterator in `app/util.py`.
- `GET /login` — redirect to Google OAuth2 (scope `userinfo.email`,
  `response_type=code`); `GET /oauth2callback` — exchange code, store access token in
  session; `GET /login-with-google` — fetch userinfo with the token and return it.
- `GET /user/<google_id>` — list that user's saved decks (JSON).
- `POST /user/?json=...&google_id=...` — insert a user deck, return the new row as JSON.
- `PUT /user/?json=...&deck_id=...` — update a deck's JSON.
- `DELETE /user/<deck_id>` — delete a deck.
- `app/cacheagent.py`: `get_most_searched_decks()` — top 1000 keyword/deck rows ordered
  by `times_searched` (module only; not routed).

## Frontend behavior (deckjam.coffee) — implement exactly

- A `Quizlet` class with a lunr index (`decks_by_id`) over fields `terms`,
  `definitions`, `title`, `description`, ref `id`.
- Keyword input `#specificKeyword` (comma-separated) with **YUI autocomplete sourced
  from Wikipedia opensearch** (`action=opensearch`, limit 10, comma queryDelimiter);
  submitting fetches `/decks/<term>` per term, appends rendered decks, adds each deck's
  JSON to the lunr index (terms and definitions joined by spaces).
- Rendering: Handlebars template `#deckTemplate` — per deck a `.deck` container with
  `data-qid` = Quizlet id, a Remove button, title + term count, then `.card` rows of
  `span.term` / `span.definition`. A second `#selectedCards` template previews
  "Append to existing deck", "Save to my decks", "Export to Quizlet" buttons.
- **Selection**: clicking a `.card` toggles `.selected`; mouse-down + drag paints the
  same toggle state across cards; mouse-up/leave ends the gesture. Selected cards get
  the light-grey background.
- **Filter**: input `#filter` (also YUI-autocompleted from the lunr corpus tokens);
  submitting searches the lunr index and `.hide()`s decks whose `qid` is not in
  results; an empty filter shows all decks.
- **Reset** button clears the deck list; per-deck **Remove** removes that deck.
- **Export**: collects `.card.selected` terms/definitions, zips them into
  `[[term, definition], ...]` pairs, `JSON.stringify`s the result (initially logged to
  console).
- `util.coffee` helpers: `strip`, `toDict`, `clone`, `zip`.
- SCSS (`all.scss`): decks get a 4px red top border, 40px bottom margin, disabled
  user-select and transitions; `.term` bold; `.termCount` small/light grey; `.selected`
  light grey (`#999`).

## UI layout

- Bootstrap 3 styled forms: a "Login With Google" primary button, keyword field labeled
  "Specific Keyword (comma separated) [required]" (placeholder: "Entropy, Enthalpy,
  Boltzmann distribution"), Submit / Reset / Export buttons, and a second "Filter Decks
  (comma separated)" field; deck containers stream below inside `#decks`.
- Page title "Deck Builder"; meta description "Deck Builder allows users to merge
  quizlet decks efficiently."

## Acceptance criteria

1. `python dev.py` serves the app; visiting `/` shows the login button, keyword and
   filter forms with working autocomplete.
2. Searching a new keyword hits Quizlet once, stores decks, and renders them; repeating
   the same keyword within a week serves from MySQL (no API call).
3. Filter box hides/shows decks via the lunr index; empty filter restores all decks.
4. Click and drag-select toggle card selection with correct highlight.
5. Export logs/produces JSON pairs of exactly the selected cards.
6. `/login` completes the Google flow; `/login-with-google` returns the userinfo JSON.
7. `/user/` CRUD round-trips a deck JSON for a `google_id` against `UserDecks`.
8. `create.sql` is idempotent (drops tables/procedure first) and applies cleanly.
9. No secret values are committed — only the `__config.py` names appear in code.
