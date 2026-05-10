# Automated Backups & Celery

The E-Squirell project utilizes Celery and Redis to handle asynchronous and scheduled tasks.

## Nightly Database Backups

A new Celery Beat scheduled task (`backup-database-nightly`) has been configured to automatically back up the PostgreSQL database every night at 2:00 AM.

### How it works:
1. Celery Beat triggers the `backup_database` task in `backend/energy_tracker/tasks.py`.
2. The task executes the `pg_dump` command-line utility directly against the database using the `DATABASE_URL` environment variable.
3. The resulting `.sql` file is saved with a timestamp (e.g., `backup_20260510_020000.sql`).

### Where are the backups stored?
The backups are saved to the `/app/backups/` directory inside the Celery worker container.
Because the backend code directory is mapped to the host machine via `docker-compose.yaml` (`./backend:/app`), you will find your backups natively on your host machine at:
```text
./backend/backups/
```

You can use these `.sql` files to restore the database or to seed new development environments.
