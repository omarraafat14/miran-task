# Docker Compose commands
build:
	@docker stop $$(docker ps -q) || true
	@docker compose -f local.yml up --build
up:
	@docker stop $$(docker ps -q) || true
	@docker compose -f local.yml up
down:
	@docker compose -f local.yml down
start:
	@docker compose -f local.yml start
stop:
	@docker compose -f local.yml stop
restart:
	@docker compose -f local.yml restart
test:
	@docker compose -f local.yml run web pytest

# Logs
logs:
	@docker compose -f local.yml logs -f

# Docker cleaning
docker-clean:
	@docker compose -f local.yml down -v --remove-orphans
	@docker system prune -f

# Container shell access
shell-web:
	@docker compose -f local.yml exec web bash

shell-db:
	@docker compose -f local.yml exec db bash

# Redeploy
redeploy-staging:
	bash redeploy-staging.sh
redeploy-prod:
	bash redeploy-prod.sh


# Django management command shortcut
manage:
	@python manage.py $(filter-out $@,$(MAKECMDGOALS))

migrations:
	@python manage.py makemigrations $(filter-out $@, $(MAKECMDGOALS))

migrate:
	@python manage.py migrate $(filter-out $@, $(MAKECMDGOALS))

superuser:
	@python manage.py createsuperuser

# Add some more useful Django commands
collectstatic:
	@python manage.py collectstatic --noinput

makemessages:
	@python manage.py makemessages -a

compilemessages:
	@python manage.py compilemessages

model:
	@python manage.py create_model

# Linting and formatting
lint:
	@flake8
	@black --check .
	@isort --check-only .

format:
	@black .
	@isort .

# Database operations
db-shell:
	@python manage.py dbshell

# Python shell
shell:
	@python manage.py shell < $(filter-out $@, $(MAKECMDGOALS))

# Dependency management
requirements:
	@pip freeze > requirements/local.txt


# Cleaning
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "*.egg" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +

# Help target
help:
	@echo "Docker Commands:"
	@echo "build          - Build and start containers"
	@echo "up             - Start containers"
	@echo "down           - Stop and remove containers"
	@echo "start          - Start existing containers"
	@echo "stop           - Stop containers"
	@echo "restart        - Restart containers"
	@echo "test           - Run tests"
	@echo "logs           - View logs"
	@echo "docker-clean   - Clean Docker resources"
	@echo ""
	@echo "Django Commands:"
	@echo "migrations     - Create migrations"
	@echo "migrate        - Apply migrations"
	@echo "superuser      - Create superuser"
	@echo "shell          - Django shell"
	@echo "db-shell       - Database shell"
	@echo "requirements   - Update requirements file"
	@echo "collectstatic  - Collect static files"
	@echo "makemessages   - Make messages"
	@echo "compilemessages - Compile messages"
	@echo "clean          - Remove Python cache files"
	@echo "lint           - Run linting checks"
	@echo "format         - Format code"
	@echo ""
	@echo "Deployment Commands:"
	@echo "redeploy-staging - Redeploy to staging"
	@echo "redeploy-prod    - Redeploy to production"





.PHONY: build up down start stop restart test lint format migrations migrate superuser shell db-shell requirements logs clean docker-clean help redeploy-staging redeploy-prod shell-web shell-db