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

SSH_KEY = ~/.ssh/django-oracle/ssh-key-2026-10-08.key
SSH_HOST = ubuntu@130.162.215.174
APP_DIR = /home/ubuntu/django_store
WEB_DIR = /var/www/django_store

ssh:
	ssh -i $(SSH_KEY) $(SSH_HOST)

copy-prod:
	ssh -i $(SSH_KEY) $(SSH_HOST) mkdir -p $(APP_DIR)
	scp -i $(SSH_KEY) compose.yml compose.prod.yml $(SSH_HOST):$(APP_DIR)/
	scp -i $(SSH_KEY) .env.prod $(SSH_HOST):$(APP_DIR)/.env
	ssh -i $(SSH_KEY) $(SSH_HOST) chmod 600 $(APP_DIR)/.env

host-dirs:
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo mkdir -p $(WEB_DIR)/staticfiles $(WEB_DIR)/media
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo chown -R 1000:1000 $(WEB_DIR)/staticfiles $(WEB_DIR)/media

host-ports:
	ssh -i $(SSH_KEY) $(SSH_HOST) 'sudo iptables -C INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT || sudo iptables -I INPUT 5 -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT'
	ssh -i $(SSH_KEY) $(SSH_HOST) 'sudo iptables -C INPUT -p tcp -m state --state NEW -m tcp --dport 443 -j ACCEPT || sudo iptables -I INPUT 6 -p tcp -m state --state NEW -m tcp --dport 443 -j ACCEPT'
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo netfilter-persistent save

nginx:
	scp -i $(SSH_KEY) deploy/nginx/zamovua.shop.conf $(SSH_HOST):/tmp/zamovua.shop.conf
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo mv /tmp/zamovua.shop.conf /etc/nginx/sites-available/zamovua.shop
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo ln -sfn /etc/nginx/sites-available/zamovua.shop /etc/nginx/sites-enabled/zamovua.shop
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo rm -f /etc/nginx/sites-enabled/default
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo nginx -t
	ssh -i $(SSH_KEY) $(SSH_HOST) sudo systemctl reload nginx
