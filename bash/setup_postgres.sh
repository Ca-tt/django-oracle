#!/bin/bash

# ----------------------------
# Config - change these values
# ----------------------------
DB_NAME="django_store"
DB_USER="hero"
: "${DB_PASSWORD:?Set DB_PASSWORD}"
DB_HOST="localhost"
DB_PORT="5432"
# ----------------------------

# 1. Create PostgreSQL database and user with settings
echo "Creating PostgreSQL database and user..."
psql -U postgres <<EOF
-- Create database
CREATE DATABASE $DB_NAME;

-- Create user
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';

-- Set default settings for user
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
EOF

# 2. Inform about Django settings
echo "Make sure DATABASES in settings.py points to PostgreSQL!"

# 3. Run Django migrations
echo "Running migrations..."
poetry run python manage.py migrate

