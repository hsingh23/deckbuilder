# AGENTS.md — working guide for coding agents

DeckJam is a small, archived **Python 2.7 Flask** app that searches, merges, and exports
Quizlet flashcard decks. Read [README.md](README.md) first for the product overview.

## Ground truth about this repo

- **Python 2.7 only.** The code uses `urllib2`, `xrange`, `unicode` bare, and
  `except URLError, e` syntax. It will not run on Python 3 without a port.
- **The Quizlet 2.0 API is dead** (retired 2018). Any feature touching
  `api.quizlet.com/2.0` needs a replacement data source before it can work.
- **Config is gitignored.** `app/__config.py` must exist with the names listed in the
  README (Google OAuth pair, Quizlet key, MySQL DSN) or imports crash at startup.
- History was rewritten messages-only on 2026-09-08 (see CHANGELOG.md note). Expect
  rewritten hashes; the local branch `backup/pre-docs-20260908` holds the originals.

## Commands

```bash
python dev.py                    # dev server on 0.0.0.0:5000, debug=True
pip install -r requirements.txt  # 2014 pins; not pruned, most entries unused
mysql ... < create.sql           # (re)create schema + stored procedure
python -m nose app/test_quizlet.py   # the one test module (2014-era nose)
```

Asset pipeline (Flask-Assets/webassets) compiles `static/coffee/*.coffee` and
`static/scss/all.scss` into `static/gen/` at first request — needs `coffee`/`sass` on PATH
or the filters fail; committed `gen/` output lets the app serve without them.

## Architecture map

```
request → Flask app (app/__init__.py, asset bundles registered)
        → views.py ─ index (Jinja+Handlebars), /decks/<kw> (JSON), /combinations, OAuth
        → quizlet.py ─ get_decks(kw):
              Keywords row (get_or_create) → expired(>1 week)/new/empty?
                yes → Quizlet search+fetch → callproc create_or_update_quizlet (upsert)
              read back Keywords ⋈ KeywordsQuizletDecks ⋈ QuizletDecks as dicts → JSON
        → userdeck_views.py ─ /user/... REST CRUD on UserDecks (google_id-keyed)
        → db.py ─ ONE shared MySQLdb connection cached on app.config["connection"];
                   query_one/query_all open+close cursors per call
```

Frontend: `static/coffee/deckjam.coffee` — Quizlet class fetches `/decks/<term>`, renders
via `#deckTemplate` (Handlebars), indexes decks in lunr (`decks_by_id`), filter box hides
non-matching decks, drag/click multi-selects `.card` elements, Export zips selected
term/definition pairs to JSON. YUI autocomplete (Wikipedia opensearch) on both inputs.

Database (`create.sql`): `Users(google_id PK, name, picture_url, email, preference)`,
`Keywords(keyword_id, keyword, last_updated, times_searched)`,
`QuizletDecks(quizlet_id PK, json MEDIUMTEXT)` — raw Quizlet JSON blobs, NOT normalized —
`UserDecks(deck_id, google_id, json, lat, lng)`, join tables `KeywordsQuizletDecks`
(with `terms_selected`, `times_deck_selected` counters) and `KeywordsUserDecks`;
stored procedure `create_or_update_quizlet(quizlet_id, keyword_id, json)` upserts.

## Conventions (as practiced in this repo)

- Routes return `flask.Response` with explicit mimetype `application/json`; raw
  parameterized SQL via the `db.py` helpers (no ORM).
- Frontend logic lives in CoffeeScript under `app/static/coffee/`; templates use
  Handlebars inside Jinja `{% raw %}` blocks; keep the two template systems separated.
- Vendored JS/CSS lives in `app/static/js|css` — do not add CDN script tags beyond the
  YUI loader already in `index.html`.

## Gotchas

- `db.py` caches the MySQL connection on `app.config` — it is never closed and is shared
  across requests; a second connection with a DictCursor once caused the
  "multiple connections" bug fixed in 9977f06. Don't reintroduce parallel connections.
- `userdeck_views.py` routes have bugs as-committed: `GET /user/<google_id>` runs
  `query_all` with a missing `= %s` placeholder and passes a bare string (not a tuple);
  PUT/POST read from `request.args` (query string) rather than the body; `update` uses
  `cursor.lastrowid` on an UPDATE. Treat it as a 2014 draft.
- `views.py` `authorized()` contains a leftover `from IPython import embed; embed()`
  breakpoint; `deckjam.coffee` contains a `debugger` statement. Remove before any reuse.
- `quizletdeck.py` is pseudo-code (mixed Python/JS syntax) kept for reference — never
  imported.
- `app/.fulltext` is a pasted Angular docs snippet, not project code.
- requirements.txt contains system packages (Landscape-Client, python-apt, ...) from a
  `pip freeze` on the droplet; don't "fix" pins blindly.
- Deploy path assumptions are hard-coded: `/var/www/deckbuilder/` in `deckbuilder.wsgi`,
  `/home/deckbuilder/...` in the old CGI shebang.

## Verifying changes

1. `python dev.py` boots without import errors (needs `app/__config.py` + MySQL up).
2. `curl localhost:5000/decks/<cached-keyword>` returns JSON (or a Quizlet-shaped error
   now that the API is gone).
3. `python -m nose app/test_quizlet.py` for the quizlet module.
4. `git diff --stat` — this repo has no CI; review by eye and keep diffs minimal.

## Pointers

- [CHANGELOG.md](CHANGELOG.md) — commit-by-commit history (what/when).
- [architectural-diary/](architectural-diary/main.md) — the *why*: schema redesigns,
  deployment pivots, caching strategy.
- [prompt.md](prompt.md) — full spec to recreate the app from nothing.
