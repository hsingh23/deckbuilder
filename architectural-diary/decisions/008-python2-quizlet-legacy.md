# ADR 008 — Staying on Python 2 and the Quizlet 2.0 API (archival posture)

- **Date:** original choice throughout 2014; posture adopted 2026-09-08
- **Status:** accepted — the repository is preserved as-is, documented but not revived

## Context

Development stopped in April 2014 when the course ended. The code is Python 2.7
(`urllib2`, print statements, `except X, e`, `unicode`), pins Flask 0.10.1 and
MySQL-python 1.2.3, and talks exclusively to the Quizlet 2.0 public API with client-id
query-parameter auth — an API and auth model Quizlet retired in 2018. The 2014
requirements.txt even freezes droplet system packages (Landscape-Client, python-apt).

## Decision

Do not port, do not "modernize opportunistically". Keep the tree byte-identical, add
documentation (README, AGENTS.md, CHANGELOG, this diary, prompt.md), and record what a
revival would actually require.

## Consequences

- The repo stays a faithful artifact of 2014 Flask/MySQL/CoffeeScript practice.
- A revival needs, at minimum: a Python 3 port of `app/` (small: ~350 lines of Python),
  a MySQL driver swap (MySQL-python → PyMySQL/mysqlclient), a Quizlet API replacement
  or alternative flashcard source behind the `get_decks` interface, and OAuth token
  validation instead of the raw `urllib2` userinfo call.
- Known landmines are catalogued in AGENTS.md (embed() breakpoint, `debugger` statement,
  malformed user-deck SQL, pseudo-code `quizletdeck.py`).
