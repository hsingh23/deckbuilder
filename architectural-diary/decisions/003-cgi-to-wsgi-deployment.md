# ADR 003 — From CGI hacks to Apache mod_wsgi on DigitalOcean

- **Date:** 2014-04-24 – 2014-04-25 (35b5920 → 89f2b11 → 7683814 → a786121 → 0d01e9d → b13085b → 8b0fa17)
- **Status:** superseded by time (domain and droplet are long gone); the artifacts remain

## Context

The project started as university coursework on EWS (engineering web hosting), which only
offered CGI. Five commits in one day (35b5920, 89f2b11, 7683814, a786121, 0d01e9d)
fight that environment: an `.htaccess` rewrite to `deckbuilder.cgi`, a wsgiref
`CGIHandler` entry point, virtualenv activation from the CGI shebang, and finally
restructuring the whole project into an importable `app/` package so CGI imports worked.

## Decision

Abandon CGI entirely when a DigitalOcean droplet became available (b13085b):
delete `deckbuilder.cgi`, add `deckbuilder.wsgi` exposing `application` (8b0fa17 fixed
the import), and check in an Apache vhost (`deckbuilder.virtualhost`) serving
`deckjam.com` from `/var/www/deckbuilder` with `/static` aliased. The CGI-era package
restructure (0d01e9d) was kept — it is why the app is a package today.

## Consequences

- The `app/` package layout, `dev.py` launcher, and `deckbuilder.wsgi` all date from the
  CGI scramble; they survived because they are good ideas independent of CGI.
- Deployment is hard-coded to droplet paths (`/var/www/deckbuilder/`) — a
  containerization or any server move would need to parameterize them.
- The `.htaccess` remains in the tree as a relic of the EWS attempt.
