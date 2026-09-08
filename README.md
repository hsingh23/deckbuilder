# DeckJam (deckbuilder)

DeckJam is a flashcard **deck builder**: search [Quizlet](https://quizlet.com) for existing
decks by keyword, pull them into a single page, filter and multi-select the individual
cards you want, and export the merged selection as JSON — or save it as a personal deck
tied to your Google account.

It was built in spring 2014 by Harsh Singh and Hilal Habashi as a course project and
deployed to a DigitalOcean droplet at `deckjam.com` behind Apache/mod_wsgi.

> **Status: archived / unmaintained.** The code targets Python 2.7 and the Quizlet 2.0
> public API (client-id query-param auth), which Quizlet retired in 2018. The app will
> not run against today's Quizlet without a new data source. It remains a clean, small
> example of a Flask + MySQL + CoffeeScript app of that era.

## Why it exists

Studying for an exam usually means juggling several overlapping Quizlet decks. DeckJam
lets you enter keywords (e.g. "Entropy, Enthalpy, Boltzmann distribution"), fetch every
matching deck into one view, keep only the cards you actually need, and export the
result — instead of manually re-typing flashcards into a new deck.

## Features

- **Keyword deck search** — fetches up to 50 Quizlet sets per keyword through a server-side
  `/decks/<keyword>` endpoint and renders them with a Handlebars template.
- **MySQL cache layer** — search results are stored as raw Quizlet JSON per keyword with a
  one-week freshness window (`Keywords.last_updated`), so repeat searches hit the database,
  not the Quizlet API. A stored procedure (`create_or_update_quizlet`) upserts decks.
- **Client-side filtering** — every fetched deck is indexed with lunr.js; the filter box
  hides decks whose terms/definitions/title don't match.
- **Keyword autocomplete** — YUI autocomplete backed by the Wikipedia opensearch API,
  comma-delimited for multi-keyword entry.
- **Drag multi-select** — click or drag across cards to toggle selection; selected cards
  are highlighted.
- **Export** — zips selected terms/definitions into JSON pairs in the console (a
  "selected cards" template previews save-to-deck and export-to-Quizlet actions).
- **Google OAuth login** — Flask-OAuth flow (`/login` → `/oauth2callback`) storing the
  access token in the session and fetching the userinfo profile.
- **User decks API** — REST endpoints (`GET/POST/PUT/DELETE /user/...`) to save, list,
  update, and delete personal decks keyed by Google `google_id`.

## Stack

| Layer | Choice | Version (pinned) |
|---|---|---|
| Language | Python | 2.7 (`urllib2`, `unicode`, `xrange`) |
| Web framework | Flask | 0.10.1 |
| Assets | Flask-Assets / webassets | 0.9 (CoffeeScript + SCSS + jsmin filters) |
| Auth | Flask-OAuth (Google) | 0.12 |
| Database | MySQL via MySQL-python (MySQLdb) | 1.2.3 |
| JSON | simplejson | (with Flask 0.10.1) |
| Frontend language | CoffeeScript | compiled by webassets |
| JS libs | jQuery 1.11.0, Handlebars 1.3.0, lunr.js, Underscore.js, YUI 3.16 | vendored under `app/static/js` |
| CSS | Bootstrap 3 + custom SCSS | vendored |
| Serving | Apache 2 + mod_wsgi (`deckbuilder.wsgi`) | DigitalOcean droplet |

## Quickstart (historical)

```bash
# 1. Python 2.7 virtualenv
virtualenv venv && source venv/bin/activate
pip install -r requirements.txt   # note: manifest is unpruned; most entries unused

# 2. Configuration — create the gitignored app/__config.py, e.g.
#    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, QUIZLET_CLIENT_KEY,
#    DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_DATABASE

# 3. Database
mysql -u root -p < create.sql     # creates tables + create_or_update_quizlet procedure

# 4. Run
python dev.py                     # serves on 0.0.0.0:5000 with debug on
```

Production used `deckbuilder.wsgi` under Apache; see `deckbuilder.virtualhost` for the
`deckjam.com` vhost and static alias.

## Project structure

```
app/
  __init__.py          Flask app factory, asset bundles (dev/prod JS, SCSS)
  views.py             index, /decks/<keywords>, /combinations, Google OAuth routes
  userdeck_views.py    REST CRUD for personal decks (/user/...)
  quizlet.py           keyword cache pipeline: search Quizlet, upsert JSON, read back
  userdeck.py          UserDecks table helpers
  db.py                shared MySQLdb connection + query_one/query_all/make_dicts
  cacheagent.py        get_most_searched_decks (top-1000 by search count)
  util.py, utils.py    keyword combinations iterator, JSONP decorator
  templates/           base.html, index.html (Handlebars deck templates)
  static/coffee/       deckjam.coffee (UI logic), util.coffee
  static/scss|css|js|gen/  styles, vendored libs, compiled output
create.sql             schema: Users, Keywords, QuizletDecks, UserDecks + join tables
deckbuilder.wsgi       mod_wsgi entry point
deckbuilder.virtualhost  Apache vhost for deckjam.com
dev.py                 local dev server launcher
requirements.txt       pip freeze from 2014 (unpruned)
```

## Environment / configuration

All configuration lives in the **gitignored** `app/__config.py` module (imported via
`from __config import *` / `app.config`). Required names:

- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` — Google OAuth app credentials
- `QUIZLET_CLIENT_KEY` — Quizlet 2.0 API client id
- `DATABASE_HOST`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_DATABASE` — MySQL

No values are committed to the repository.

## Deploy URLs (as of 2014)

- Production site: `http://deckjam.com/` (Apache vhost in `deckbuilder.virtualhost`)
- Decks search API: `/decks/<keyword>` — JSON array of cached Quizlet decks
- Keyword combinations: `/combinations?k=a,b,c`
- Login: `/login` → Google → `/oauth2callback`
- User decks: `/user/<google_id>` (GET), `/user/` (POST/PUT), `/user/<deck_id>` (DELETE)

## Further reading

- [CHANGELOG.md](CHANGELOG.md) — every commit, newest first
- [AGENTS.md](AGENTS.md) — how to work in this codebase
- [architectural-diary/main.md](architectural-diary/main.md) — why it looks the way it does
- [prompt.md](prompt.md) — one-shot prompt that would recreate this app from scratch
