# DineFlow ERP — Production Deployment & Operations Guide

This guide details the deployment, configuration, and maintenance procedures for hosting DineFlow in single-outlet and multi-branch commercial environments.

---

## 1. System Requirements

- **Operating System**: Linux (Ubuntu 22.04 LTS / Debian 12 / RHEL 9) or Windows Server 2022 / Windows 11 Pro.
- **Python**: Python 3.12+ (64-bit).
- **RAM**: Minimum 4GB (8GB recommended for concurrent POS & KDS terminals).
- **Disk**: 20GB SSD storage.
- **Network**: Local Area Network (LAN) with Gigabit switch for POS, KDS, and printer connectivity.

---

## 2. Quickstart & Local Setup

```bash
# 1. Clone repository & navigate into workspace
git clone <repository_url>
cd dineflow

# 2. Initialize and activate Python virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database schema migrations
python manage.py migrate

# 5. Hydrate database with complete Indian restaurant master data & train AI model
python manage.py seed_dineflow

# 6. Verify automated test suite (41 tests)
python manage.py test tests

# 7. Start local development server
python manage.py runserver 0.0.0.0:8000
```

---

## 3. Production Hardening Configuration

Create a `.env` configuration file in the project root:

```env
# Security
DEBUG=False
SECRET_KEY=generate-a-strong-random-50-character-secret-key-here
ALLOWED_HOSTS=dineflow.local,pos.royalnizam.in,192.168.1.100,127.0.0.1

# Localization
TIME_ZONE=Asia/Kolkata
LANGUAGE_CODE=en-in

# Database (Default: SQLite WAL mode, or PostgreSQL)
DATABASE_URL=sqlite:///db.sqlite3
```

### Enable SQLite Write-Ahead Logging (WAL) Mode
For high concurrency across POS and KDS terminals on SQLite:
```python
# In settings.py or via sqlite CLI
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA busy_timeout=5000;
```

---

## 4. Production Web Server Architecture

In production, DineFlow runs behind an Nginx reverse proxy with Gunicorn (Linux) or Waitress (Windows).

### 4.1 Gunicorn Systemd Service (`/etc/systemd/system/dineflow.service`)
```ini
[Unit]
Description=DineFlow Restaurant ERP Application Server
After=network.target

[Service]
User=dineflow
Group=www-data
WorkingDirectory=/var/www/dineflow
ExecStart=/var/www/dineflow/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 4 \
          --bind 127.0.0.1:8000 \
          dineflow.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4.2 Nginx Reverse Proxy Configuration (`/etc/nginx/sites-available/dineflow`)
```nginx
server {
    listen 80;
    server_name dineflow.local 192.168.1.100;

    location /static/ {
        alias /var/www/dineflow/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /var/www/dineflow/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5. Operations & Health Commands

| Command | Purpose |
| :--- | :--- |
| `python manage.py check_dineflow_health` | Audits database integrity, outlet counts, catalog size, and ML weights |
| `python manage.py export_gst_summary --month 9 --year 2026` | Summarizes monthly statutory Indian GST collections (CGST/SGST/IGST) |
| `python manage.py seed_dineflow` | Seeds master data and retrains the Scikit-Learn demand forecasting engine |
| `python manage.py test tests` | Executes the complete 41-test automated suite across all domain apps |
