---

## name: deploy
description: >-
  Prepare and deploy this Django and PostgreSQL project to an Oracle Cloud
  Infrastructure server with Docker, GitHub Actions tests, and CI/CD.
  Product images stay on a host directory served by Nginx. Use when the user
  mentions deploy, Oracle Cloud, OCI, Docker, or CI.

# Deploy

One Always Free OCI Ubuntu VM. App and PostgreSQL in Docker. Host Nginx for TLS, `/static/`, and `/media/`. Product images live on a host directory bind-mounted into the app container. Poetry for deps. Secrets only in env vars, never in git or the image.

Settings: `django_store.settings.dev` locally, `django_store.settings.prod` on the server. Follow the steps in order.

## 1. App

`base.py` / `dev.py` / `prod.py` already exist. Extend them; do not invent a second settings layout.

- Add `gunicorn`. Keep `django-browser-reload` in the main dependencies; dev settings enable it only while `DEBUG` is on.
- `base.py` keeps `FileSystemStorage` for media (`MEDIA_ROOT` = `BASE_DIR / "media"`) and `StaticFilesStorage` for static files. Do not add `django-storages`. `prod.py` sets `DEBUG = False` and `STATIC_ROOT` only. Dev serves `/media/` while `DEBUG` is on. Production does not: Nginx serves that path.
- Keep reading `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DB_*`, and Google OAuth from the environment. Add `CSRF_TRUSTED_ORIGINS`. Do not introduce `DATABASE_URL`.
- Update `.env.example` for every new variable (empty secrets). Real `.env` stays untracked.
- Leave HTTPS cookie flags off until TLS exists. `collectstatic` is an explicit command, not startup.



## 2. Docker

Multi-stage `Dockerfile` on Python 3.13: `base` installs from the lock file, `prod` is the runtime image. Non-root; Gunicorn on `django_store.wsgi:application` at `0.0.0.0:8000`. Add `.dockerignore`. Match the VM CPU architecture. PostgreSQL 17 everywhere.

- `compose.yml`: shared web and Postgres (`env_file`, `DB_HOST=db`, app at `127.0.0.1:8000`, named volume, healthcheck).
- `compose.dev.yml`: dev settings, project bind-mounted, Postgres on `127.0.0.1:5433`. Use `compose -f compose.yml -f compose.dev.yml`.
- `compose.prod.yml`: published image, Postgres on the compose network only, bind-mounted `staticfiles` and `media` for Nginx. The media mount is writable by the container user. Recreating the container must not delete it. Use `compose -f compose.yml -f compose.prod.yml`.
- Container command is Gunicorn only. Run `migrate` and `collectstatic` as separate commands.



## 3. GitHub tests

`.github/workflows/ci.yml` on every PR and push: Poetry + deps, PostgreSQL 17 service, `poetry run python manage.py test`. No lint/type-check job. No deploy yet.

## 4. OCI

- Network. SSH is open only from your IP. Ports 80 and 443 are open. Port 5432 is closed. The public IP is reserved, so it stays the same if you stop the VM.
- SSH works. From your machine: `ssh -i <private-key> ubuntu@<public-ip>`.
- Docker and Compose are installed on the VM.
- App directory holds `compose.yml`, `compose.prod.yml`, and a production `.env` filled in from `.env.example`.
- Host directories exist: `/var/www/django_store/staticfiles` and `/var/www/django_store/media`. `media` must be writable by uid 1000.
- A boot-volume snapshot is scheduled, so product images survive if the VM is replaced.

## 5. Nginx and TLS

DNS A record → public IP. Nginx on the host → `127.0.0.1:8000`. Serve `/static/` and `/media/` from the host directories. Do not proxy `/media/` to Gunicorn. Issue a cert, redirect HTTP → HTTPS, then enable secure cookies and set `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS`. Update Google OAuth callback URLs.

## 6. CI/CD

On push to `master`, after tests: build/push `ghcr.io/<owner>/<repo>:<sha>` and `:latest`; SSH to the VM; pull, `compose -f compose.yml -f compose.prod.yml up -d`, `migrate`, `collectstatic`; fail if `127.0.0.1:8000` does not respond. App secrets stay in the server `.env`. Keep the previous SHA tag for rollback (`compose` with that tag).

## 7. Check

Tests pass; master deploys; HTTPS, admin, and OAuth work; static loads; a product image is on the host media directory and still loads after the app container is recreated; Postgres data persists; `5432` is closed; rollback to the previous tag works.