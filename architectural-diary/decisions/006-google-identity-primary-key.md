# ADR 006 — Google identity via google_id as the Users primary key

- **Date:** 2014-04-26 – 2014-04-29 (325e625, 7a477cc, 65df640)
- **Status:** accepted

## Context

Decks are personal: "my decks" must survive across browsers and sessions. The project
had no email infrastructure for verification and wanted zero-friction login for a
student audience, so a local password flow was never considered seriously (Flask-Security
sits unused in requirements.txt).

## Decision

Adopt Google OAuth2 via Flask-OAuth (`/login` → Google consent → `/oauth2callback`),
keep the access token in the Flask session, and fetch the userinfo profile. Make
`Users.google_id` (an int) the table's **primary key** (7a477cc), storing `name`,
`picture_url`, `email`, `preference` alongside; `UserDecks.google_id` references it.
No local credential storage at all.

## Consequences

- Login is one redirect; no password handling or reset flows to build or secure.
- The whole identity model is hostage to Google and to the 2014 OAuth2 flow (implicit
  `response_type=code` with `userinfo.email` scope; the `urllib2` userinfo fetch in
  `login_with_google` predates modern token verification).
- Changing Google accounts loses your decks; there is no account-merge path.
- `authorized()` kept a leftover IPython `embed()` breakpoint (65df640) — an artifact of
  interactive debugging that made it into master.
