# Changelog

All notable changes to the deckbuilder (DeckJam) project. Newest first.

> **Note on history:** On 2026-09-08 the git history on `master` was rewritten
> with a **messages-only** rewrite (`git filter-branch --msg-filter`) to replace
> vague legacy commit subjects (e.g. `idk`, `yo`, `changes`, `if only`) with
> descriptive conventional-commit messages. File contents, trees, authors, and
> dates are byte-for-byte unchanged; only commit messages differ. All commit
> hashes below refer to the rewritten history. A pre-rewrite snapshot is kept
> locally on branch `backup/pre-docs-20260908` (never pushed).

## 2014-04-30

- **4cdb34d — feat: wire up deck filtering and selected-card export** (Harsh Singh)
  - Rename `all.coffee` to `deckjam.coffee`; add `filterDecks` handler that searches the lunr index and shows/hides deck divs, and an Export handler that zips selected cards' terms/definitions to JSON.
  - Add `util.coffee` helpers (strip, toDict, clone, zip), fix the deck template to read `this.json.*`, add a `selectedCards` template and YUI autocomplete, and rebuild `gen/coffee.js`.

- **c9704b3 — Merge google-oauth branch; serve decks via /decks endpoint** (Harsh Singh)
  - Integrate Google OAuth (login button, `/login-with-google`, userinfo fetch) with master.
  - Frontend fetches decks from the local `/decks/<term>` route instead of calling the Quizlet API directly; replaces `show_ids` with a `show_only` filter.

- **203e69d — Merge user-deck feature branch into master** (Harsh Singh)
  - Integrate the user-deck modules (`userdeck.py`, `userdeck_views.py`, `cacheagent.py`, `utils.py`) and the `google_id` foreign-key change with the single-keyword search refactor on master.

- **ec32887 — feat: add REST user-deck endpoints keyed by google_id** (Harsh Singh)
  - Add `app/userdeck_views.py` with GET/POST/PUT/DELETE routes under `/user/` backed by `UserDecks`, a `jsonp` decorator in `app/utils.py`, and register the module from `views.py`.
  - Change the `UserDecks` foreign key from `user_id` to `google_id` in `create.sql`; drop lunr field boosts in the frontend.

- **c29f5db — refactor: support a single keyword per deck search** (Harsh Singh)
  - Change `quizlet.get_decks` to take one keyword instead of iterating a comma-separated list, returning a flat deck list instead of a keyword-keyed dict.
  - Remove the commented-out general-keyword input from `index.html`.

## 2014-04-29

- **551e8c8 — feat: track keyword search counts, add cacheagent module** (Hilal Habashi)
  - Increment `Keywords.times_searched` on every deck search via `update_times_searched` in `quizlet.py`; add `times_searched` column plus `cacheagent.py` with `get_most_searched_decks` (top 1000 by search count).
  - Rename `update_userdeck` to `_userdeck` in `userdeck.py`.

- **65df640 — feat: expose Google login button and fetch userinfo** (Harsh Singh)
  - Add a Login With Google button to `index.html`, rename `/index2` to `/login-with-google`, and fetch the Google userinfo endpoint with the access token.
  - Adds `Users(google_id, ...)` table to the schema.

- **57a9379 — refactor: reduce userdeck.py to UserDecks CRUD helpers** (Hilal Habashi)
  - Remove the Quizlet keyword/fetch pipeline duplicated from `quizlet.py`.
  - Add `save_to_db` (INSERT), update-by-deck_id, and `delete_from_db` (DELETE); key the existing read on `user_id`.

- **7fcd595 — feat: add userdeck.py to fetch user decks by email** (Hilal Habashi)
  - Add `app/userdeck.py` modeled on `quizlet.py`'s keyword pipeline, selecting `json` from `UserDecks` by owner email so user-created decks can be loaded.

## 2014-04-27

- **9977f06 — fix: replace dual MySQL connections with per-query cursor helpers** (Harsh Singh)
  - Remove the separate DictCursor connection from `app/db.py` (source of the multiple-connection bug) and add `make_dicts`/`query_one`/`query_all` helpers that open and close cursors on the single shared connection.
  - Fix inverted keyword-expiry comparison, decode stored deck JSON on read, and use MEDIUMTEXT plus `DROP PROCEDURE IF EXISTS` in `create.sql`.

- **0252ff1 — fix: repair index page asset bundle and deck loading** (Harsh Singh)
  - Point `base.html` at the `all_dev_js` bundle instead of missing bundles; give the CoffeeScript sub-bundle an explicit output target.
  - Guard stored deck JSON decoding, return results from `create_decks_from_quizlet`, make `QuizletDecks.quizlet_id` a primary key and `Keywords` UNSIGNED.

## 2014-04-26

- **882af45 — Merge branch 'master' of github.com:hsingh23/deckbuilder** (Harsh Singh)
  - Standard merge syncing local master with GitHub (schema and requirements work from both sides).

- **7a477cc — feat: key Users table on google_id with profile columns** (Harsh Singh)
  - Replace auto-increment `user_id` with `google_id` as the `Users` primary key; add `picture_url`, `email`, and `preference` columns.

- **c9c710c — feat: add Google OAuth login flow** (Harsh Singh)
  - Configure flask_oauth's google remote app with credentials from `__config`; add `/login`, `/oauth2callback` (stores the access token in the session), and a route that fetches the Google userinfo endpoint.

- **99e556d — refactor: rename quizlet_backup to quizlet, add dict cursors** (Harsh Singh)
  - Move the working implementation back to `app/quizlet.py` and update imports; switch `views.py` to simplejson.
  - Add DictCursor-backed connection helpers in `db.py` so rows return as dicts in `get_decks_from_database`.

- **e24d849 — refactor: consolidate Quizlet backend into working quizlet_backup module** (Harsh Singh)
  - Replace the broken `quizlet.py` and `quizlet-backup.py` drafts with a functional module: `get_or_create_keyword` with weekly `last_updated` expiry and upserts via the new `create_or_update_quizlet` stored procedure.
  - Update `create.sql` (rename `created` to `last_updated`, add selection-count columns, define the procedure); remove the Quizlet client key from client-side CoffeeScript.

- **6687681 — Merge branch 'usedb' of github.com:hsingh23/deckbuilder into usedb** (Harsh Singh)
  - Standard merge syncing the usedb feature branch with GitHub.

- **27abb10 — docs: drop user_id from QuizletDecks schema comment** (Harsh Singh)
  - Fix the table-summary comment in `create.sql` to match the actual `QuizletDecks(quizlet_id, json)` definition.

- **475a701 — refactor: remove duplicate queryQuizletDecks from quizlet-backup.py** (Hilal Habashi)
  - Delete the trailing `queryQuizletDecks` function, which duplicated the `get_decks` flow and called undefined helpers.

- **1873f04 — Merge branch 'usedb' of https://github.com/hsingh23/deckbuilder into usedb** (Hilal Habashi)
  - Standard merge syncing the usedb branch over HTTPS.

- **4307592 — feat: add quizlet-backup.py draft for deck fetch and DB cache** (Hilal Habashi)
  - Sketch a rewritten Quizlet handler: database lookup with weekly fetch-date freshness check, Quizlet API search/fetch, and a draft `save_to_db`. Work-in-progress, not yet imported.

## 2014-04-25

- **1166460 — Merge branch 'master' of github.com:hsingh23/deckbuilder into usedb** (Harsh Singh)
  - Standard merge bringing master's CGI/deployment fixes into usedb.

- **486756a — Merge branch 'usedb' of github.com:hsingh23/deckbuilder into usedb** (Harsh Singh)
  - Standard merge syncing the usedb branch with GitHub.

- **ef16cc3 — fix: correct Quizlet DB query, cursor use, and keyword parsing** (Harsh Singh)
  - Fetch a cursor before executing the keyword lookup and join through `KeywordsQuizletDecks` to `QuizletDecks`.
  - Lowercase/strip keywords, drop `sort=most_studied` from set search, and format fetched sets as (id, json) tuples.

- **0ef0fe6 — refactor: consolidate JS/coffee asset bundles, drop unused files** (Harsh Singh)
  - Rework webassets bundles so dev and prod each inline compiled CoffeeScript into `gen/dev.js` and minified `gen/packed.js`.
  - Delete unused `app/forms.py` and `server.py`; fix virtualhost indentation; run the app directly from `app/__init__.py`.

- **8b0fa17 — fix: expose Flask app as WSGI application in deckbuilder.wsgi** (Harsh Singh)
  - Import the app from the app package as `application` so mod_wsgi can find the callable; the bare `import server` defined none.

- **036f783 — refactor: rename mysql.query to connection.execute in quizletdeck** (Hilal Habashi)
  - Replace all `mysql.query` calls with `connection.execute`, drop the `get_parsed` placeholder stub, and add an empty `app/preferences.py` stub.

- **0e92d19 — chore: ignore Vim *.swp swap files** (Harsh Singh)
  - Add `*.swp` to `.gitignore`.

- **b13085b — build: switch deployment from CGI to Apache WSGI for DigitalOcean** (Harsh Singh)
  - Remove `deckbuilder.cgi`; add `deckbuilder.wsgi` plus an Apache virtualhost (deckjam.com) under `/var/www/deckbuilder`.
  - Simplify `server.py`; ignore `venv/`.

## 2014-04-24

- **0d01e9d — fix: restructure into importable app package for CGI deployment** (Harsh Singh)
  - Add `app/__init__.py` constructing the Flask app, loading the gitignored `__config`, registering asset bundles, and importing views.
  - Rename the top-level launcher to `dev.py` and slim `server.py`; point `deckbuilder.cgi` at `server`.

- **a786121 — chore: add server.py launcher with rotating-file logging** (Harsh Singh)
  - Add an executable entry point running the Flask dev server with a RotatingFileHandler logging to `deckbuilder.log` for deployment debugging.

- **7683814 — fix: run CGI app from project virtualenv** (Harsh Singh)
  - Rename the launcher to `app.py` so the CGI `import app` resolves; point the CGI shebang at the project virtualenv python and activate it.
  - Drop the scratch `yolo.txt`.

- **128cc21 — chore: merge usedb branch into cgi line** (Harsh Singh)
  - Merge the db-prep changes (get_connection rename, quizletdeck.py stub reformat) into the CGI deployment branch.

- **89f2b11 — fix: correct CGI entry point module import** (Harsh Singh)
  - Import the real `app` module in `deckbuilder.cgi` instead of the nonexistent `yourapplication`; guard the dev-server `app.run()` behind `__main__`.

- **35b5920 — build: add CGI deployment config for EWS hosting** (Harsh Singh)
  - Add `.htaccess` rewrite rules routing non-file requests to a new `deckbuilder.cgi` entry point running the Flask app via wsgiref's CGIHandler.

## 2014-04-22

- **9b82612 — refactor: prep db and quizlet modules for database integration** (Harsh Singh)
  - Rename `get_cursor` to `get_connection` in `db.py` and update call sites.
  - Reformat `quizletdeck.py` pseudocode into indented snake_case stubs ready for real MySQL calls.

- **7fcf750 — refactor: return MySQL connection instead of cursor from db helper** (Harsh Singh)
  - Hand back the shared MySQLdb connection so callers can use `with con:` for automatic commit/rollback on errors.

- **84d20aa — chore: merge coffeescript dev branch into master** (Harsh Singh)
  - Merge the CoffeeScript/Handlebars UI work (search UI, YUI autocomplete, lunr filtering, JSON-cache schema, vendored assets) into master.

- **42b54c4 — chore: remove tracked .pyc bytecode files** (Harsh Singh)
  - Delete compiled bytecode files now that `*.py[oc]` is ignored via `.gitignore`.

- **ce385be — feat: add keyword autocomplete and lunr deck filtering, rework schema** (Harsh Singh)
  - Plug YUI autocomplete (Wikipedia opensearch) into keyword and filter inputs; index fetched decks with lunr.js for client-side filtering.
  - Rewrite `create.sql` as Users/Keywords/QuizletDecks/UserDecks tables caching raw Quizlet JSON instead of normalized Card/Deck rows; serve `/decks/<keywords>` as JSON and add a `/combinations` endpoint; improve drag-to-select card interactions.

## 2014-04-18

- **224e667 — chore: remove webassets cache files committed by mistake** (Harsh Singh)
  - Delete `app/static/.webassets-cache/*` Flask-Assets cache artifacts accidentally added in the previous commit.

- **6e82bec — feat: add client-side CoffeeScript/Handlebars deck search UI** (Harsh Singh)
  - Add the CoffeeScript Quizlet class searching the Quizlet API and rendering decks with a Handlebars template on the index page.
  - Rewrite `base.html` to serve SCSS/JS/Coffee through Flask-Assets bundles; add SCSS styles for decks, cards, and selection highlighting.

## 2014-03-31

- **f1ffcc7 — chore: remove keyword form from index template** (Harsh Singh)
  - Strip the keyword input form from the index template while the search flow was being redesigned for the client-side UI.

## 2014-03-21

- **e439b4c — feat: scaffold Flask deck-builder with Quizlet search and MySQL cache** (Harsh Singh)
  - Initial commit: Flask skeleton with views, a `/decks` endpoint backed by a WTForms keyword form, `quizlet.py` to search the Quizlet 2.0 API by keyword and merge results into MySQL, and a `db.py` connection helper cached on `app.config`.
  - `create.sql` schema for keywords/decks/cards plus join tables; base/index templates with Bootstrap/jQuery static assets and a nose test stub.

## 2026-09-08

- **docs: add README, AGENTS.md, CHANGELOG, architectural diary, and one-shot recreation prompt**
  - Full documentation pass: README, agent guide, this changelog, decision diary, and a one-shot recreation prompt.
