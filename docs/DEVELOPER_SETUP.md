# Developer Setup

Welcome to the E-Squirell project! To streamline local development, we have automated the environment initialization and provided a `Makefile` with common commands.

## Prerequisites
- Docker & Docker Compose
- `make`

## Initial Setup
Before running the application for the first time, you must initialize the local HTTPS certificates and configure your host machine's DNS resolution. 

Run the following command from the root of the project:
```bash
make setup
```

**What `make setup` does:**
1. Checks if `mkcert` is installed, and installs it via `apt` if missing.
2. Installs the local Certificate Authority (`mkcert -install`).
3. Generates SSL certificates for `e_squirell.home` and places them in `~/e_squirell_certs` (this is where `docker-compose.yaml` expects them).
4. Appends `127.0.0.1 e_squirell.home` to your `/etc/hosts` file (this step will prompt for your sudo password).

## Running the Application
Once setup is complete, you can start the entire stack (Frontend, Backend, Postgres, Redis, Celery, MQTT) with:
```bash
make dev
```
You can then access the application at `https://e_squirell.home`.

## Other Commands
- `make test`: Runs the pytest test suite in the backend container.
- `make clean`: Tears down all containers, networks, and wipes all associated Docker volumes. **Use with caution!**
