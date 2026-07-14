# Site Visit Log API

Last Updated: 2026-07-13 (session 7)

## Purpose

A learning exercise that extends the previous single-table `users` CRUD API into a
two-table, one-to-many API for a fictional heritage consultant. The consultant
records `Site` records (buildings or places under observation) and `Visit` records
(dated inspections tied to exactly one site). The exercise's real purpose is to
practise PostgreSQL, Docker Compose, environment-based configuration, SQLAlchemy's
modern declarative syntax, one-to-many relationships, foreign keys, and Alembic
migrations from the start.

## Goal

A working FastAPI service, backed by PostgreSQL via Docker Compose, implementing
the `Site` → `Visit` one-to-many relationship with foreign keys, managed by Alembic
migrations from the first commit, exposing the endpoints listed below.

## Project Type

Python backend / API learning project (FastAPI + PostgreSQL + SQLAlchemy + Alembic)

## Audience / User

Joseph, working through this as a self-directed learning exercise. The "heritage
consultant" persona is the fictional use case the API is modelled around, not a
real client.

## Deliverables

- FastAPI app with `Site` and `Visit` models in SQLAlchemy's declarative style
- `docker-compose.yml` running PostgreSQL for local development
- Environment-based configuration (database URL etc. via environment variables)
- Alembic set up from the start, with migration history reflecting schema changes
- Endpoints:
  - `POST /sites/`
  - `GET /sites/`
  - `GET /sites/{site_id}`
  - `POST /sites/{site_id}/visits/`
  - `GET /sites/{site_id}/visits/`
  - `GET /visits/`
  - `GET /visits/?since=2026-01-01`
- Tests covering the above

## Current Status

Part 1 (Setup, Docker, Configuration, Database, Alembic) is complete, and
`README.md` documents it in full. Part 2 is complete through step 11: all
three site routes and the two nested visit routes (`POST`/`GET
/sites/{site_id}/visits/`) are implemented in `app/main.py`, with schemas in
`app/schemas.py`. Reviewed against the Part 2 manual with no outstanding
discrepancies — two bugs found and fixed (`VisitCreate.weather` mistyped as
`str` instead of `str | None`; `read_site` missing a `Session` type hint).
No automated tests yet — `tests/test_sites.py` is still empty. Steps 12–15
(flat `/visits/` filter, `psql` join inspection, `follow_up_required`
migration) are next.

## Folder Structure

```text
site_visit_log_api/
  PROJECT.md
  .gitignore
  app/            # FastAPI application code (models, schemas, routers, main.py)
  tests/          # pytest test suite
  docs/           # any supporting notes or API design docs
  _me/
    journal.md
    tasks.md
    decisions.md
```

## Epistemic State

### Known Facts

- Previous project (`users` CRUD) used FastAPI and SQLite, with dependencies
  tracked in `requirements.txt`.
- Relationship shape is fixed by the brief: `Site 1 ───< Visit`, with
  `visits.site_id` as a foreign key to `sites.id`.
- Update and delete routes are intentionally omitted — the learning goals are
  relationships, foreign keys, migrations, configuration and testing, not full
  CRUD repetition.
- The endpoint list in Deliverables is the complete target surface for this
  exercise.

### Working Assumptions

- Alembic will be used with its autogenerate workflow against the SQLAlchemy
  models, rather than hand-written migrations — confirmed or invalidated by: how
  the first migration is created.
- `pytest` (plus `httpx`/FastAPI's `TestClient`) will be the test runner, matching
  typical FastAPI testing practice — confirmed or invalidated by: when the test
  suite is first set up.
- PostgreSQL will run via Docker Compose only for local development, with no
  separate staging/production config needed — confirmed or invalidated by: whether
  deployment ever enters scope (currently explicitly out of scope).

### Open Questions

- Will any code or structure be carried over from the previous `users` CRUD
  project, or is this fully separate?
- Any constraint on PostgreSQL version, or is "latest stable" acceptable for the
  Docker Compose service?

### Out of Scope

- Many-to-many relationships — deliberately excluded by the brief to keep focus on
  one-to-many first.
- Controlled vocabularies and hierarchical tags — not needed for a two-table
  exercise.
- Faceted search — beyond the `?since=` filter on `/visits/`, no search layer.
- Authentication — no auth layer for this exercise.
- Frontend — API only.
- Asynchronous database access — synchronous SQLAlchemy only.
- Deployment — local Docker Compose only, no hosting.
- Update and delete routes for `Site`/`Visit` — explicitly omitted by the brief.

## Working Principles

- Migrations from the start: every schema change goes through an Alembic
  revision, never a manual `ALTER` or a dropped/recreated table — the point of
  this exercise is learning the migration workflow itself.
- Config over hardcoding: the database URL and any other environment-specific
  values come from environment variables, never a hardcoded connection string —
  this is one of the named learning goals.
- Relationship correctness over convenience: the foreign key and any cascade
  behaviour between `Site` and `Visit` should be modelled deliberately, not left
  to whatever SQLAlchemy defaults to without a conscious choice.
- Scope discipline: resist adding update/delete routes, auth, or many-to-many
  complexity — the brief excludes these on purpose so the relationship, migration
  and configuration mechanics stay the focus.
- Reinforce, don't switch: where a technique was already used in the previous
  project (FastAPI, `requirements.txt`), keep using it the same way rather than
  swapping tools, so the repetition builds fluency rather than fragmenting it.

## Decisions in Force

- 2026-07-11: Use FastAPI as the framework, reinforcing the previous project
  rather than introducing a new one.
- 2026-07-11: Use `pip` + `requirements.txt` for dependency management, reinforcing
  the previous project's tooling.
- 2026-07-11: Set up folder structure and project tracking only at this stage — no
  application code, `docker-compose.yml`, or Alembic config yet. Joseph will write
  these himself as the learning exercise.
- 2026-07-11: Stop the Docker container (`docker compose down`) at the end of
  each session and restart the venv + container fresh each time, rather than
  leaving Postgres running continuously — deliberate practice of the command
  sequence since it isn't yet muscle memory.

## Next Steps

- Implement `GET /visits/` with `?since=` filter (Part 2 step 12).
- Inspect the `Site`/`Visit` join directly in `psql` (Part 2 step 13).
- Add `follow_up_required` to `Visit` via a second migration, then wire it
  into the schemas and create-visit route (Part 2 steps 14–15).
- Write automated tests for the site endpoints, then the visit endpoints.

## Session Protocol

At the start of a session:

1. Read `PROJECT.md`, `_me/journal.md`, and `_me/tasks.md`.
2. Summarise current status and next steps in 2-3 sentences.
3. Continue from the user's chosen task.

At the end of a session:

1. Update Current Status and Next Steps in `PROJECT.md`.
2. Add a dated entry to `_me/journal.md`.
3. Update `_me/tasks.md`.
4. Add any significant decisions to `_me/decisions.md` and to Decisions in Force above.

## Changelog

- 2026-07-11: Project created.
- 2026-07-11: Directory structure audited against Part 1 manual — confirmed
  complete and matching. Dependency list corrected (psycopg[binary],
  pydantic-settings, per manual).
- 2026-07-11: Part 1 manual steps 1–13 completed — dependencies, Docker
  Compose PostgreSQL running, `.env` populated, settings module written.
- 2026-07-11: Part 1 manual steps 14–16 completed — `app/database.py` and
  `app/models.py` written; an indentation bug that nested `Visit` inside
  `Site` was found in review, fixed, and re-verified. Pushed to git.
- 2026-07-13: Part 1 manual steps 18–21 completed — Alembic initialised and
  wired to the app (`sqlalchemy.url` from settings, `target_metadata` from
  `Base.metadata`), first migration generated and reviewed (after
  regenerating once to fix an empty `-m` message), applied with
  `alembic upgrade head`, and schema verified in `psql`. Part 1 is now fully
  complete.
- 2026-07-13: `README.md` written, covering Part 1 end to end.
- 2026-07-13: First endpoints implemented — `POST /sites/`, `GET /sites/`,
  `GET /sites/{site_id}` in `app/main.py`, with schemas in `app/schemas.py`.
  Manually tested, committed, pushed.
- 2026-07-13: Part 2 step 11 completed — nested visit routes (`POST`/`GET
  /sites/{site_id}/visits/`) added to `app/main.py`. Two bugs found in
  review and fixed: `VisitCreate.weather` mistyped as `str` instead of
  `str | None`, and a missing `Session` type hint in `read_site`. Committed,
  pushed.
