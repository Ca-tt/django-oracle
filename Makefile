# server
run:
	poetry run python manage.py runserver

# migrations
showmigrations:
	poetry run python manage.py showmigrations

migrate:
	poetry run python manage.py migrate

newapp:
	poetry run python manage.py startapp $(name)

superuser:
	poetry run python manage.py createsuperuser

psql:
	psql -U postgres -d django_store

changepass:
	poetry run python manage.py changepassword $(user)

collectstatic:
	poetry run python manage.py collectstatic --noinput

COMPOSE_DEV = docker compose -f compose.yml -f compose.dev.yml
COMPOSE_PROD = docker compose -f compose.yml -f compose.prod.yml

dev-up:
	$(COMPOSE_DEV) up --build -d

dev-down:
	$(COMPOSE_DEV) down

dev-migrate:
	$(COMPOSE_DEV) exec web python manage.py migrate

dev-superuser:
	$(COMPOSE_DEV) exec web python manage.py createsuperuser

dev-shell:
	$(COMPOSE_DEV) exec web python manage.py shell

dev-psql:
	$(COMPOSE_DEV) exec db sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB"'

prod-build:
	docker build -t $${APP_IMAGE:-django-store:latest} .

prod:
	$(COMPOSE_PROD) up -d

prod-down:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f

prod-migrate:
	$(COMPOSE_PROD) exec web python manage.py migrate

prod-collectstatic:
	$(COMPOSE_PROD) exec web python manage.py collectstatic --noinput

# git
ready:
	git add . && git commit && git push

# tests
tests:
	poetry run python manage.py test

act:
	act -j tests --reuse

act-down:
	docker ps -aq --filter name=act- | xargs -r docker rm -f

seed-categories:
	poetry run python manage.py seed_categories
