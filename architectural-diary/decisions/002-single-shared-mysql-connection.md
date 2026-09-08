# ADR 002 — One shared MySQL connection, per-query cursors

- **Date:** 2014-04-22 → 2014-04-27 (7fcf750, 837aa5b, 9977f06)
- **Status:** accepted (with a known wart: the connection is never closed)

## Context

`db.py` originally returned a *cursor* from a helper. 7fcf750 changed it to return the
*connection* so call sites could use `with con:` for automatic commit/rollback. Later a
second helper (`get_dict_connection`) opened a **separate** MySQLdb connection with a
`DictCursor` so `get_decks_from_database` could get dict rows — and the app started
failing with the "multiple connections" bug (two connections, interleaved transactions),
fixed in bcd1198/9977f06.

## Decision

Keep **exactly one** MySQLdb connection, cached on `app.config["connection"]`, created
lazily on first use. All reads go through small helpers (`query_one`, `query_all`) that
open a cursor, run, and close it immediately; dict rows are produced in Python by
`make_dicts(cursor, rows)` from `cursor.description`, not by a special cursor class.
Writes use an explicit cursor plus `cursor.connection.commit()`.

## Consequences

- The connection-bug class disappeared; every statement sees a consistent session.
- Under mod_wsgi this is one connection per worker process, held forever — fine for a
  course-project droplet, unacceptable at scale.
- `make_dicts` duplicates what `DictCursor` does, by hand — a small price accepted to
  keep a single connection.
