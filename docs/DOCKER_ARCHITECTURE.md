# Docker Architecture

The E-Squirell project uses a multi-container Docker setup orchestrated via `docker-compose`.

## Backend Initialization (Auto-migrations)
The Django backend container is configured with a custom `entrypoint.sh`. 
Before the web server starts, the entrypoint will automatically run `python manage.py migrate`. This ensures that whenever you pull new code with model changes, your database schema is automatically kept in sync without manual intervention.

## Database Seeding (Auto-seeding)
The PostgreSQL database container (`postgres`) is configured to auto-seed using the standard `/docker-entrypoint-initdb.d/` feature.

If you ever wipe your Docker volumes using `make clean` or `docker compose down -v`, the very next time you run `make dev`, PostgreSQL will automatically restore the `backup_20260423_192239.sql` file.

This ensures that developers always have a populated database with historical data to work with when initializing the project.
