include .env.local
export

.PHONY: dev-db-start dev-db-stop dev-db-reset run-service

dev-db-start:
	@echo "Starting the development database..."
	@if ! psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='$(DB_USER)'" | grep -q 1; then \
		echo "Creating user '$(DB_USER)'..."; \
		psql -U postgres -c "CREATE USER $(DB_USER) WITH PASSWORD '$(DB_PASSWORD)';"; \
	fi
	@if ! psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='$(DB_NAME)'" | grep -q 1; then \
		echo "Creating database '$(DB_NAME)'..."; \
		psql -U postgres -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"; \
	fi
	@echo "Database '$(DB_NAME)' is ready on port $(DB_PORT)."

dev-db-reset: dev-db-start
	@echo "Resetting the development database..."
	@psql -U postgres -c "DROP DATABASE IF EXISTS $(DB_NAME);"
	@psql -U postgres -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"
	@echo "Database '$(DB_NAME)' has been reset."

run-service:
	@echo "Starting the user service..."
	DATABASE_URL=postgresql://$(DB_USER):$(DB_PASSWORD)@localhost:$(DB_PORT)/$(DB_NAME) uvicorn src.main:app --reload
