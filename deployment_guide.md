# Deployment Guide - House Price Prediction Web App

This guide explains how to configure and deploy the House Price Prediction Web Application to various hosting targets.

---

## 1. Prerequisites & Environment Setup

Ensure the target server or cloud runtime has **Python 3.9+** (preferably **3.11**) installed.

### Configuration Variables
Set the following environment variables in your deployment dashboard or production `.env`:
* `SECRET_KEY`: A unique secure string for session encryption.
* `DEBUG`: Set to `False` in production.
* `ALLOWED_HOSTS`: Comma-separated domains mapping to your app (e.g. `valuer-ai.onrender.com,localhost`).
* `DATABASE_URL`: (Optional) PostgreSQL database connection string (e.g. `postgres://user:pass@host:5432/db`). If omitted, the app defaults to local SQLite.

---

## 2. Deploying to Render (Recommended PaaS)

Render is fully compatible with Django and provides free/low-cost tiers for web services and Postgres databases.

1. **Log in to Render** and select **New +** -> **Web Service**.
2. **Connect your Repository** (GitHub/GitLab).
3. **Configure Service Details**:
   * **Name**: `ames-valuer-ai`
   * **Language**: `Python 3`
   * **Branch**: `main`
   * **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python prediction/train_model.py
     ```
     *(Note: Running `train_model.py` in the build step ensures the best model pickle `house_price_model.pkl` is pre-trained and saved before startup.)*
   * **Start Command**: `gunicorn house_price_prediction.wsgi`
4. **Add Environment Variables**:
   * Open the **Environment** tab and add the variables listed in section 1 above (e.g., `SECRET_KEY`, `DEBUG=False`).
5. **Deploy**: Render will trigger the build pipeline, train the ML models, configure static assets, and boot the Gunicorn server.

---

## 3. Deploying to Railway

Railway auto-detects `Procfile` configurations, making it extremely fast to deploy.

1. **Create a project** in Railway and choose **Deploy from GitHub**.
2. **Add variables** under the **Variables** tab (e.g., `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=*`).
3. **Automatic Database Connection**:
   * If you provision a PostgreSQL instance in the same Railway project, Railway automatically injects `DATABASE_URL` into your web service, allowing Django to switch to PostgreSQL instantly!
4. **Custom Build Command (if needed)**:
   * By default, Railway runs the `Procfile` start command. Ensure migration and training script runs are executed upon release. You can specify a custom release phase or combine commands in the `Procfile` if needed (e.g., `python manage.py migrate && python prediction/train_model.py && gunicorn house_price_prediction.wsgi`).

---

## 4. Deploying to PythonAnywhere

PythonAnywhere is a dedicated Python hosting service using WSGI configs.

1. **Clone the Repo**: In a PythonAnywhere Bash Console, clone the repo:
   ```bash
   git clone <your-repo-url>
   cd House-Price
   ```
2. **Create a Virtual Environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 ames-env
   pip install -r requirements.txt
   ```
3. **Initialize Database & Model**:
   ```bash
   python manage.py migrate
   python prediction/train_model.py
   ```
4. **Configure Web Tab**:
   * Go to the **Web** tab on PythonAnywhere and create a new web app choosing **Manual Configuration** and Python version **3.11**.
   * Set **Virtualenv path** to `/home/<username>/.virtualenvs/ames-env`.
   * Open the **WSGI Configuration File** and modify it to point to Django:
     ```python
     import os
     import sys

     path = '/home/<username>/House-Price'
     if path not in sys.path:
         sys.path.append(path)

     os.environ['DJANGO_SETTINGS_MODULE'] = 'house_price_prediction.settings'

     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
5. **Static Files mapping**:
   * Under the **Web** tab, map `/static/` URL to `/home/<username>/House-Price/staticfiles/` (after running `python manage.py collectstatic`).

---

## 5. Deploying to a Linux VPS (Ubuntu/Nginx/Gunicorn)

For self-hosted Linux VPS services:

1. **Install OS dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx git -y
   ```
2. **Setup virtual env & install dependencies**:
   ```bash
   git clone <repo-url> /var/www/ames-valuer
   cd /var/www/ames-valuer
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python prediction/train_model.py
   python manage.py collectstatic --noinput
   ```
3. **Configure Systemd Gunicorn Service**:
   Create `/etc/systemd/system/gunicorn.service`:
   ```ini
   [Unit]
   Description=Gunicorn daemon for Ames Valuer
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/var/www/ames-valuer
   ExecStart=/var/www/ames-valuer/.venv/bin/gunicorn --workers 3 --bind unix:/var/www/ames-valuer/ames.sock house_price_prediction.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
   Start and enable Gunicorn:
   ```bash
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```
4. **Configure Nginx Proxy**:
   Create `/etc/nginx/sites-available/ames-valuer`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       location /static/ {
           root /var/www/ames-valuer;
       }
       location /media/ {
           root /var/www/ames-valuer;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/ames-valuer/ames.sock;
       }
   }
   ```
   Enable site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/ames-valuer /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```
