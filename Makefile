.PHONY: setup dev test clean

setup:
	@echo "Running setup script..."
	@bash bin/setup.sh

dev:
	@echo "Starting development environment..."
	docker compose up --build -d

test:
	@echo "Running tests..."
	docker compose run --rm backend pytest

clean:
	@echo "Cleaning up docker volumes and orphans..."
	docker compose down -v --remove-orphans
