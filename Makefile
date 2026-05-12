# Doctor AI Agent - developer shortcuts
# Usage: make <target>

COMPOSE ?= docker-compose

.PHONY: help
help:  ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ----------------------------------------------------------------------------
# Docker Compose
# ----------------------------------------------------------------------------
.PHONY: up down build logs restart ps
up:        ## Start the full stack (build + detached)
	$(COMPOSE) up --build -d

down:      ## Stop the stack
	$(COMPOSE) down

build:     ## Build images
	$(COMPOSE) build

logs:      ## Tail logs from all services
	$(COMPOSE) logs -f --tail=100

restart:   ## Restart the stack
	$(COMPOSE) restart

ps:        ## List running containers
	$(COMPOSE) ps

# ----------------------------------------------------------------------------
# Backend (run inside the backend container)
# ----------------------------------------------------------------------------
.PHONY: migrate makemigrations seed shell createsuperuser test lint-back
migrate:          ## Apply database migrations
	$(COMPOSE) exec backend python manage.py migrate

makemigrations:   ## Create new migrations from model changes
	$(COMPOSE) exec backend python manage.py makemigrations

seed:             ## Seed demo data (demo@doctor.com / demo1234)
	$(COMPOSE) exec backend python manage.py seed_data

shell:            ## Open a Django shell
	$(COMPOSE) exec backend python manage.py shell

createsuperuser:  ## Create an admin user
	$(COMPOSE) exec backend python manage.py createsuperuser

test:             ## Run pytest
	$(COMPOSE) exec backend pytest -q

# ----------------------------------------------------------------------------
# Frontend (run inside the frontend container)
# ----------------------------------------------------------------------------
.PHONY: npm-install type-check lint-front build-front
npm-install:   ## Install frontend dependencies
	$(COMPOSE) exec frontend npm install

type-check:    ## Run TypeScript type-check
	$(COMPOSE) exec frontend npm run type-check

lint-front:    ## Run Next.js ESLint
	$(COMPOSE) exec frontend npm run lint

build-front:   ## Build the Next.js app
	$(COMPOSE) exec frontend npm run build

# ----------------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------------
.PHONY: bootstrap
bootstrap: up migrate seed  ## First-time setup: build, migrate, seed
	@echo ""
	@echo "Ready."
	@echo "  Frontend: http://localhost:3000"
	@echo "  API:      http://localhost:8000/api/v1/"
	@echo "  Swagger:  http://localhost:8000/api/docs/"
	@echo "  Admin:    http://localhost:8000/admin/"
	@echo ""
	@echo "  Demo: demo@doctor.com / demo1234"
