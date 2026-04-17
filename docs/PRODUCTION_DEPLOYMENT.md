# E-Squirell — Production Deployment Guide

> **Target machine:** Raspberry Pi 5 (8 GB RAM) running Raspberry Pi OS (64-bit) or Ubuntu Server 24.04 on your local network.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Raspberry Pi OS Setup](#2-raspberry-pi-os-setup)
3. [Install Docker & Docker Compose](#3-install-docker--docker-compose)
4. [Clone the Repository](#4-clone-the-repository)
5. [Set Up GitHub Actions Self-Hosted Runner](#5-set-up-github-actions-self-hosted-runner)
6. [Configure Environment Variables](#6-configure-environment-variables)
7. [Prepare Required Directory Structure](#7-prepare-required-directory-structure)
8. [Generate SSL Certificates (HTTPS)](#8-generate-ssl-certificates-https)
9. [Configure Local DNS (Domain Resolution)](#9-configure-local-dns-domain-resolution)
10. [First Deploy — Build & Start the Stack](#10-first-deploy--build--start-the-stack)
11. [Create Django Superuser](#11-create-django-superuser)
12. [Schedule Celery Tasks](#12-schedule-celery-tasks)
13. [Verify Everything is Working](#13-verify-everything-is-working)
14. [Deploying Code Changes (CI/CD)](#14-deploying-code-changes-cicd)
15. [Service URLs Quick Reference](#15-service-urls-quick-reference)

---

## 1. Prerequisites

- Raspberry Pi 5 imaged and reachable over SSH
- Static IP assigned to the Pi on your local network  
  *(recommended: set a DHCP reservation in your router for the Pi's MAC address)*
- Git installed on the Pi

---

## 2. Raspberry Pi OS Setup

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y git curl ca-certificates gnupg netcat-openbsd mkcert
```

---

## 3. Install Docker & Docker Compose

```bash
# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the Docker repo (use 'ubuntu' instead of 'debian' if running Ubuntu)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Allow your user to run Docker without sudo
sudo usermod -aG docker $USER

# Log out and back in, then verify
docker --version
docker compose version
```

---

## 4. Clone the Repository

```bash
# Clone into the home directory (production compose uses ~/e_squirell paths)
cd ~
git clone https://github.com/gonzur75/e_squirell.git
cd e_squirell
```

---

## 5. Set Up GitHub Actions Self-Hosted Runner

The Pi acts as a **self-hosted GitHub Actions runner**. It connects outbound to GitHub and waits for jobs — no port forwarding or VPN required. This is a one-time setup.

### Register the Runner

1. Go to your GitHub repository → **Settings → Actions → Runners**
2. Click **New self-hosted runner**
3. Select **Linux** / **ARM64** (for Pi 5)
4. GitHub will show you a set of commands — run them on the Pi:

```bash
# Create a dedicated directory for the runner
mkdir -p ~/actions-runner && cd ~/actions-runner

# Download the runner (check GitHub for the exact latest URL shown in the UI)
curl -o actions-runner-linux-arm64.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.x.x/actions-runner-linux-arm64-2.x.x.tar.gz

tar xzf ./actions-runner-linux-arm64.tar.gz

# Configure (use the token GitHub shows you in the UI — it expires in 1 hour)
./config.sh --url https://github.com/gonzur75/e_squirell --token <YOUR_TOKEN>
```

### Install as a System Service (auto-starts on boot)

```bash
# Install and enable the runner service
sudo ./svc.sh install
sudo ./svc.sh start

# Verify it's running
sudo ./svc.sh status
```

Back in GitHub → Settings → Runners, the Pi should now appear as **Idle** (green dot).

> **Note:** The runner runs as your user and inherits your Docker permissions. Make sure
> `docker` group membership is applied (`groups` should include `docker`) before installing the service.

---

## 6. Configure Environment Variables

The backend requires a `.env` file. A template is provided at `backend/env/.env-default`.

```bash
# Copy the template
cp ~/e_squirell/backend/env/.env-default ~/e_squirell/backend/env/.env

# Edit it with your real values
nano ~/e_squirell/backend/env/.env
```

Fill in **all** values:

```env
# Django
DEBUG=False
SECRET_KEY=<generate a long random string — use: python3 -c "import secrets; print(secrets.token_urlsafe(50))">
DJANGO_ALLOWED_HOSTS=e_squirell.home,localhost,127.0.0.1,<PI_IP_ADDRESS>

# Django superuser (created automatically on first run)
DJANGO_SU_NAME=admin
DJANGO_SU_EMAIL=admin@local.home
DJANGO_SU_PASSWORD=<choose a strong password>

# Tuya Smart Meter credentials (from your Tuya account)
SM_ID=<your_device_id>
SM_IP=<your_device_local_ip>
SM_KEY=<your_device_local_key>

# PostgreSQL
POSTGRES_USER=e_squirell
POSTGRES_PASSWORD=<choose a strong password>
POSTGRES_DB=e_squirell_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

> **Note:** `POSTGRES_HOST=postgres` must be exactly `postgres` — that is the Docker service name, not an IP address.

---

## 7. Prepare Required Directory Structure

The production backend mounts a log file from the host. Create it before starting:

```bash
# Create logs directory and the log file
mkdir -p ~/logs
touch ~/logs/app.toml
```

---

## 8. Generate SSL Certificates (HTTPS)

This step installs a local Certificate Authority (CA) that your browser will trust, removing the "Not Secure" warning.

```bash
# Install mkcert's CA into the system and browser trust stores
# (run once per machine)
mkcert -install

# Create the certificate directory
mkdir -p ~/e_squirell_certs

# Generate the certificate for your local domain
mkcert \
  -key-file ~/e_squirell_certs/key.pem \
  -cert-file ~/e_squirell_certs/cert.pem \
  e_squirell.home localhost 127.0.0.1
```

> **Important:** If you also access the dashboard from other devices on your network (e.g., your laptop or phone), you need to install the mkcert CA on those devices too, OR use the Pi's IP address directly and add it to the cert. See [Accessing from Other Devices](#accessing-from-other-devices) below.

### Accessing from Other devices

To access the dashboard from phones/laptops that connect to the Pi by IP:

```bash
# Re-generate the cert including the Pi's static IP (e.g. 192.168.1.100)
mkcert \
  -key-file ~/e_squirell_certs/key.pem \
  -cert-file ~/e_squirell_certs/cert.pem \
  e_squirell.home localhost 127.0.0.1 192.168.1.100
```

Then copy the CA root certificate to other devices:
```bash
# The CA cert is at (on the Pi):
mkcert -CAROOT
# → typically: /home/marcin/.local/share/mkcert/rootCA.pem

# Copy to your laptop and import it into your OS/browser trust store
```

---

## 9. Configure Local DNS (Domain Resolution)

The dashboard is served at `https://e_squirell.home`. Every device that accesses it needs to resolve that domain name to the Pi's IP address.

### Option A — Edit `/etc/hosts` (simplest, per device)

On every device that needs access:

```bash
# Replace 192.168.1.100 with your Pi's actual static IP
echo "192.168.1.100  e_squirell.home" | sudo tee -a /etc/hosts
```

### Option B — Router DNS (recommended, works for all devices automatically)

Log into your router's admin panel and add a **custom DNS entry** (sometimes called "static DNS" or "local DNS"):
- **Hostname:** `e_squirell.home`
- **IP Address:** `<Pi's static IP>`

This avoids editing `/etc/hosts` on every device.

---

## 10. First Deploy — Build & Start the Stack

```bash
cd ~/e_squirell

# Start the full production stack (builds images, starts in background)
docker compose -f docker-compose-production.yaml up --build -d
```

This starts the following services:
| Service | Description |
|---|---|
| `backend` | Django + Uvicorn ASGI server on port 8000 |
| `postgres` | PostgreSQL 17.5 database |
| `redis` | Redis 7 message broker |
| `celery-worker` | Processes async tasks |
| `celery-beat` | Schedules periodic tasks |
| `mosquitto` | MQTT broker (for ESP32 devices) |
| `frontend` | React app served via Nginx on ports 80 & 443 |

Check all services are running:

```bash
docker compose -f docker-compose-production.yaml ps
```

View logs for a specific service:

```bash
docker compose -f docker-compose-production.yaml logs -f backend
docker compose -f docker-compose-production.yaml logs -f frontend
```

---

## 11. Create Django Superuser

The `entrypoint.sh` runs migrations automatically. The superuser credentials come from the `.env` file (`DJANGO_SU_NAME`, `DJANGO_SU_EMAIL`, `DJANGO_SU_PASSWORD`).

If you need to create it manually:

```bash
docker compose -f docker-compose-production.yaml exec backend \
  python manage.py createsuperuser
```

Access Django Admin at: `https://e_squirell.home/admin/`

---

## 12. Schedule Celery Tasks

Celery Beat handles the periodic data fetching. Tasks should be configured via **Django Admin**:

1. Go to `https://e_squirell.home/admin/`
2. Navigate to **Django Celery Beat → Periodic Tasks**
3. Click **Add Periodic Task**
4. Add the following task:
   - **Name:** `Fetch Smart Meter Data`
   - **Task:** `energy_tracker.tasks.fetch_and_save_energy_data`
   - **Schedule:** Every 1 minute (Interval schedule)
5. Save

> **Alternative:** Tasks can also be defined in `backend/config/settings.py` under `CELERY_BEAT_SCHEDULE` to auto-schedule on startup.

Monitor running tasks at: `http://<PI_IP>:5555` (Flower dashboard)

---

## 13. Verify Everything is Working

```bash
# Check all containers are healthy
docker compose -f docker-compose-production.yaml ps

# Test the backend API directly
curl -k https://e_squirell.home/api/v1/energy_tracker/ | head -c 500

# Check Nginx is responding on both ports
curl -I http://e_squirell.home    # Should return 301 redirect to HTTPS
curl -Ik https://e_squirell.home  # Should return 200
```

Open in browser:
- **Dashboard:** `https://e_squirell.home` — should show 🔒 padlock
- **Django Admin:** `https://e_squirell.home/admin/`
- **Flower (Celery Monitor):** `http://<PI_IP>:5555`

---

## 14. Deploying Code Changes (CI/CD)

Deployments are **fully automated** via GitHub Actions. The self-hosted runner on the Pi listens for jobs and handles everything.

### Normal Deploy Flow

```bash
# On your development machine — merge your work into the deploy branch and push
git checkout deploy
git merge main
git push origin deploy
```

GitHub Actions will automatically:
1. Run Django tests *(informational — won't block the deploy)*
2. Check out the latest code on the Pi
3. Run `docker compose -f docker-compose-production.yaml up --build -d`
4. Clean up old Docker image layers
5. Run health checks on the backend API and frontend
6. Report success or failure in the GitHub Actions tab

### Manual Deploy (without a code push)

You can trigger a deployment at any time from the GitHub UI:
1. Go to your repository → **Actions → E-Squirell CI/CD**
2. Click **Run workflow** → select branch `deploy` → **Run workflow**

### Monitoring Deployments

- **GitHub:** Repository → Actions tab — shows live logs for every step
- **Pi (direct):** `docker compose -f docker-compose-production.yaml ps`

### Emergency Manual Deploy (if runner is down)

```bash
# SSH into the Pi and run manually
cd ~/e_squirell
git pull
docker compose -f docker-compose-production.yaml up --build -d
```

---

## 15. Service URLs Quick Reference

| URL | Service |
|---|---|
| `https://e_squirell.home` | Main Dashboard |
| `https://e_squirell.home/admin/` | Django Admin |
| `https://e_squirell.home/api/v1/energy_tracker/` | Energy Tracker API |
| `https://e_squirell.home/api/v1/storage_heater/` | Storage Heater API |
| `http://<PI_IP>:5555` | Flower (Celery task monitor) |
| `http://<PI_IP>:1883` | MQTT broker (for ESP32 devices) |

---

## Troubleshooting

### Browser still shows "Not Secure"
- Make sure you ran `mkcert -install` on the **device you're browsing from**, not just the Pi
- For phones: you need to manually install the CA certificate. Export `rootCA.pem` from `mkcert -CAROOT` and import it in your phone's settings

### Frontend container won't start
```bash
docker compose -f docker-compose-production.yaml logs frontend
# Most likely cause: ~/e_squirell_certs directory doesn't exist or cert files are missing
ls ~/e_squirell_certs/
```

### Backend fails with database error
```bash
docker compose -f docker-compose-production.yaml logs backend
# Ensure POSTGRES_HOST=postgres (the service name, not an IP)
# Ensure ~/e_squirell/backend/env/.env exists and is correct
```

### MQTT / ESP32 not connecting
- Check Mosquitto is running: `docker compose -f docker-compose-production.yaml logs mosquitto`
- Verify the Pi's IP is reachable from the ESP32 on port 1883

### "Permission denied" on logs
```bash
# The backend mounts ~/logs/app.toml — ensure it exists and is writable
touch ~/logs/app.toml
chmod 666 ~/logs/app.toml
```
