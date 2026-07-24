# MM Task Tracker — Deployment Guide

## 1. Overview

This document describes how to deploy and run the MM Task Tracker application.

The application is built using:

* Python
* FastAPI
* Uvicorn
* SQLite
* Jinja2 templates
* HTML/CSS/JavaScript
* Docker
* Docker Compose

The application can currently be run in two ways:

1. **Local Python environment**
2. **Docker / Docker Compose**

The recommended deployment approach for consistent environments is Docker Compose.

---

# 2. Project Structure

The deployment-related files are located at the project root:

```text
D:.
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
│
└── app
    ├── main.py
    │
    ├── data
    │   └── managers.py
    │
    ├── db
    │   ├── database.py
    │   ├── init_db.py
    │   └── tracker.db
    │
    ├── models
    │   ├── employee.py
    │   └── enum.py
    │
    ├── routes
    │   ├── employee.py
    │   └── manager.py
    │
    ├── services
    │   ├── manager.py
    │   └── submission_service.py
    │
    ├── static
    │   ├── manager.js
    │   ├── script.js
    │   └── style.css
    │
    └── templates
        ├── employee.html
        └── manager.html
```

---

# 3. Deployment Architecture

The current application architecture can be represented as:

```text
                 User Browser
                      │
                      │ HTTP
                      ▼
              FastAPI / Uvicorn
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    Employee Routes         Manager Routes
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
                Service Layer
                      │
                      ▼
                 SQLite DB
                      │
                      ▼
              app/db/tracker.db
```

When running with Docker:

```text
                 User Browser
                      │
                      │ HTTP
                      ▼
              Docker Container
                      │
                      ▼
              Uvicorn / FastAPI
                      │
                      ▼
                Application
                      │
                      ▼
                 SQLite DB
```

---

# 4. Prerequisites

## Local Deployment

For local deployment, install:

* Python 3.x
* pip
* Git (optional)

Verify Python:

```bash
python --version
```

Verify pip:

```bash
python -m pip --version
```

---

## Docker Deployment

For Docker deployment, install:

* Docker Desktop
* Docker Compose

Verify Docker:

```bash
docker --version
```

Verify Docker Compose:

```bash
docker compose version
```

Docker Desktop includes Docker Compose on modern installations.

---

# 5. Local Deployment

## Step 1 — Clone or Obtain the Project

Place the project on your machine.

Example:

```text
D:\MM_Task_Tracker
```

Open a terminal in the project root:

```powershell
cd D:\MM_Task_Tracker
```

The current directory should contain:

```text
Dockerfile
docker-compose.yml
requirements.txt
app
```

---

# 6. Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv .venv
```

This creates:

```text
.venv/
```

The virtual environment keeps project dependencies isolated from the system Python installation.

---

# 7. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

After activation, the terminal should show something similar to:

```text
(.venv) PS D:\MM_Task_Tracker>
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

---

# 8. Install Dependencies

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Using:

```powershell
python -m pip
```

is recommended because it ensures that pip runs through the currently active Python interpreter.

This helps avoid situations where:

```text
pip
```

points to a different Python installation or virtual environment.

---

# 9. Database Setup

The application currently uses SQLite.

The database file is:

```text
app/db/tracker.db
```

The application database architecture is:

```text
app
└── db
    ├── database.py
    ├── init_db.py
    └── tracker.db
```

The SQLite database is stored as a local file.

No separate database server is required.

---

# 10. Database Initialization

The exact initialization process depends on the implementation of:

```text
app/db/init_db.py
```

If the application requires database initialization before first startup, run the initialization script according to the project's implementation.

For example, if `init_db.py` is executable as a module:

```powershell
python -m app.db.init_db
```

Alternatively, initialization may be performed automatically by `app/main.py`.

The deployment process should ensure that the following tables exist before the application accepts requests:

```text
managers
submissions
tasks
```

---

# 11. Running the Application Locally

Start the FastAPI application using Uvicorn.

From the project root:

```powershell
uvicorn app.main:app --reload
```

The application should become available at:

```text
http://127.0.0.1:8000
```

The `--reload` option is intended for development.

It automatically reloads the server when Python source files change.

---

# 12. Accessing the Application

After starting the server, open:

```text
http://127.0.0.1:8000
```

The exact available pages depend on the route configuration in:

```text
app/main.py
```

The application contains two primary user interfaces:

```text
Employee Interface
        │
        ▼
employee.html


Manager Interface
        │
        ▼
manager.html
```

The employee and manager page URLs should be verified against the router prefixes configured in `app/main.py`.

---

# 13. FastAPI API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

These endpoints are useful for:

* Viewing registered APIs.
* Testing API endpoints.
* Inspecting request parameters.
* Inspecting request bodies.
* Inspecting API responses.

---

# 14. Local Deployment Architecture

The local development environment is:

```text
Windows
   │
   ▼
Python Virtual Environment
   │
   ▼
Uvicorn
   │
   ▼
FastAPI
   │
   ├── Routes
   ├── Services
   ├── Templates
   └── Static Files
   │
   ▼
SQLite
   │
   ▼
app/db/tracker.db
```

---

# 15. Docker Deployment

Docker packages the application and its dependencies into a container.

The deployment architecture becomes:

```text
Host Machine
    │
    ▼
Docker Engine
    │
    ▼
MM Task Tracker Container
    │
    ├── Python
    ├── FastAPI
    ├── Uvicorn
    ├── Application Code
    └── SQLite
```

---

# 16. Dockerfile

The project contains:

```text
Dockerfile
```

The Dockerfile defines how the application image is built.

The expected deployment flow is:

```text
Dockerfile
     │
     ▼
Docker Image
     │
     ▼
Docker Container
     │
     ▼
FastAPI Application
```

The Docker image should contain:

* Python runtime.
* Application dependencies.
* Application source code.
* Required templates.
* Required static files.

---

# 17. Build Docker Image

From the project root:

```powershell
docker build -t mm-task-tracker .
```

This creates a Docker image named:

```text
mm-task-tracker
```

Verify the image:

```powershell
docker images
```

---

# 18. Run Docker Container

A typical container command is:

```powershell
docker run -p 8000:8000 mm-task-tracker
```

The port mapping is:

```text
Host Port 8000
      │
      ▼
Container Port 8000
```

The application can then be accessed from:

```text
http://localhost:8000
```

---

# 19. Docker Compose Deployment

The project contains:

```text
docker-compose.yml
```

Docker Compose is the preferred way to manage the application container.

From the project root, run:

```powershell
docker compose up --build
```

This command:

1. Builds the application image.
2. Creates the container.
3. Starts the application.
4. Exposes the configured application port.

Run in detached mode:

```powershell
docker compose up --build -d
```

The `-d` option runs the application in the background.

---

# 20. Check Running Containers

Run:

```powershell
docker compose ps
```

or:

```powershell
docker ps
```

The application container should appear as running.

---

# 21. View Application Logs

To view logs:

```powershell
docker compose logs
```

To follow logs in real time:

```powershell
docker compose logs -f
```

Logs are useful for identifying:

* Application startup errors.
* Database errors.
* Python exceptions.
* Request processing errors.
* Container startup issues.

---

# 22. Stop the Application

To stop the Docker Compose application:

```powershell
docker compose down
```

This stops and removes the containers created by Docker Compose.

---

# 23. Restart the Application

To restart:

```powershell
docker compose restart
```

If application code or dependencies have changed, rebuild:

```powershell
docker compose up --build -d
```

---

# 24. SQLite Deployment Considerations

The application currently uses SQLite:

```text
app/db/tracker.db
```

SQLite is file-based.

This means the database exists inside the application's filesystem.

This is suitable for:

* Local development.
* Small deployments.
* Internal tools.
* Low to moderate concurrent usage.

However, container storage requires special consideration.

If the SQLite database is stored only inside the container filesystem, the database may be lost when the container is removed.

Therefore, production deployments should use a persistent Docker volume or bind mount.

Conceptually:

```text
Docker Container
       │
       │
       ▼
/app/app/db/tracker.db
       │
       │ Persistent Mount
       ▼
Host / Docker Volume
```

---

# 25. Recommended SQLite Volume

The database should be persisted outside the temporary container layer.

A Docker Compose configuration can use a volume for the database directory.

Conceptually:

```yaml
volumes:
  - ./app/db:/app/app/db
```

This means:

```text
Host:
./app/db

        │
        │ Mounted into container
        ▼

Container:
/app/app/db
```

The database file remains available after the container is recreated.

The exact mount path must match the working directory and paths defined in the project's `Dockerfile`.

---

# 26. Database Backup

Because SQLite is a file-based database, the primary database backup is:

```text
app/db/tracker.db
```

A basic backup can be created by copying the database file.

Example:

```powershell
Copy-Item app\db\tracker.db backups\tracker_2026-07-24.db
```

A production backup process should:

1. Create regular backups.
2. Store backups separately from the application.
3. Retain multiple backup versions.
4. Test database restoration periodically.

Recommended backup structure:

```text
backups/
├── tracker_2026-07-22.db
├── tracker_2026-07-23.db
└── tracker_2026-07-24.db
```

The `backups/` directory should not be committed to Git.

---

# 27. Production Deployment

For a production deployment, the recommended architecture is:

```text
                  Internet / Internal Network
                            │
                            ▼
                    Reverse Proxy
                 (Optional Nginx/Proxy)
                            │
                            ▼
                     FastAPI Container
                            │
                            ▼
                         Uvicorn
                            │
                            ▼
                       Application
                            │
                            ▼
                    Persistent Database
```

The application should not rely on:

```bash
uvicorn app.main:app --reload
```

for production.

The `--reload` option is intended for development.

---

# 28. Production Uvicorn Command

A production-oriented command can be:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The important difference is:

```text
--host 0.0.0.0
```

This allows the application to listen on all network interfaces inside the container.

The application can then be exposed through Docker:

```text
Host
  │
  │ Port 8000
  ▼
Container
  │
  │ Port 8000
  ▼
Uvicorn
```

---

# 29. Development vs Production

## Development

```bash
uvicorn app.main:app --reload
```

Characteristics:

* Automatic reload.
* Useful for local development.
* Not intended for production.

---

## Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Characteristics:

* No automatic reload.
* Suitable for containerized deployment.
* Can be placed behind a reverse proxy.

---

# 30. Environment Configuration

Future deployments should move environment-specific configuration out of source code.

Recommended configuration:

```text
Environment Variables
        │
        ├── DATABASE_PATH
        ├── HOST
        ├── PORT
        └── ENVIRONMENT
```

For example:

```text
ENVIRONMENT=production
DATABASE_PATH=/app/app/db/tracker.db
HOST=0.0.0.0
PORT=8000
```

The application should read these values through environment variables.

This allows the same Docker image to be used across:

```text
Development
    │
    ▼
Testing
    │
    ▼
Production
```

without modifying application source code.

---

# 31. Secrets and Sensitive Configuration

The project currently does not appear to require external secrets based on the provided architecture.

If future functionality introduces:

* API keys.
* Database passwords.
* Authentication secrets.
* External service credentials.

These values must not be hard-coded into:

```text
Python source code
Dockerfile
Git repository
```

Instead, use:

```text
Environment Variables
Docker Secrets
Secret Management System
```

The `.env` file, if introduced, should be excluded from Git:

```text
.env
```

and added to:

```text
.gitignore
```

---

# 32. Docker Ignore Rules

The project contains:

```text
.dockerignore
```

This file should exclude unnecessary files from the Docker build context.

Recommended exclusions include:

```text
.git
.gitignore
.venv
__pycache__
*.pyc
.env
backups
```

Care must be taken not to exclude required application files such as:

```text
app/templates
app/static
app/db
```

if they are required inside the container.

---

# 33. Health Checks

The application currently has an employee route that can act as a basic health check:

```text
GET /
```

However, the route currently returns:

```json
{
    "message": "Employee Routes Working!"
}
```

A dedicated health endpoint is recommended:

```text
GET /health
```

Expected response:

```json
{
    "status": "ok"
}
```

This endpoint can be used by:

* Docker health checks.
* Reverse proxies.
* Load balancers.
* Monitoring systems.

Recommended future flow:

```text
Monitoring System
       │
       ▼
GET /health
       │
       ├── 200 → Healthy
       │
       └── Error → Unhealthy
```

---

# 34. Deployment Verification

After deployment, verify the following.

## Application

```text
Application starts successfully
```

## Health

```text
GET /
```

or future:

```text
GET /health
```

## Employee Page

Verify that:

```text
employee.html
```

loads successfully.

## Manager Page

Verify that:

```text
manager.html
```

loads successfully.

## Static Files

Verify:

```text
manager.js
script.js
style.css
```

load correctly.

## Database

Verify:

```text
tracker.db
```

exists and is accessible.

## Manager Data

Verify:

```text
GET /managers
```

returns manager data.

## Submission

Submit an employee record and verify:

```text
submissions
```

and:

```text
tasks
```

are updated.

## Manager Dashboard

Verify:

* Latest submissions.
* Manager filtering.
* Date filtering.
* Idle employee list.
* Task visibility.
* Task status report.

## Lookup

Test:

```text
Employee lookup
Task lookup
```

---

# 35. Deployment Smoke Test

A basic deployment smoke test should follow this sequence:

```text
1. Start application
        │
        ▼
2. Open application
        │
        ▼
3. Open Employee Page
        │
        ▼
4. Load Manager List
        │
        ▼
5. Submit Employee Data
        │
        ▼
6. Verify Database
        │
        ▼
7. Open Manager Dashboard
        │
        ▼
8. Verify Submission
        │
        ▼
9. Test Filters
        │
        ▼
10. Test Employee Lookup
        │
        ▼
11. Test Task Lookup
        │
        ▼
12. Test Task Status Report
```

---

# 36. Updating the Deployment

When application code changes:

```text
Developer
    │
    ▼
Update Source Code
    │
    ▼
Build New Docker Image
    │
    ▼
Stop Old Container
    │
    ▼
Start New Container
    │
    ▼
Run Smoke Tests
```

Using Docker Compose:

```powershell
docker compose down
docker compose up --build -d
```

If the database is mounted using a persistent volume or bind mount, the database should remain available after container recreation.

---

# 37. Deployment Rollback

If a new deployment introduces a problem:

```text
New Version
    │
    ▼
Problem Detected
    │
    ▼
Stop New Version
    │
    ▼
Deploy Previous Image
    │
    ▼
Verify Application
```

Docker image tags should be used for production deployments.

For example:

```text
mm-task-tracker:1.0.0
mm-task-tracker:1.1.0
mm-task-tracker:1.2.0
```

This makes rollback easier than relying only on:

```text
latest
```

---

# 38. Recommended Production Improvements

Before deploying the application for long-term production use, consider implementing:

1. Dedicated `/health` endpoint.
2. Persistent SQLite volume.
3. Automated database backups.
4. Pydantic request validation.
5. Centralized error handling.
6. Structured application logging.
7. Production environment configuration.
8. Docker image versioning.
9. HTTPS through a reverse proxy.
10. Authentication for manager dashboard.
11. Authorization for manager functionality.
12. Automated tests.
13. Database migration strategy.
14. Monitoring and alerting.
15. Migration from SQLite to PostgreSQL if concurrency grows significantly.

---

# 39. Future Production Architecture

The recommended future architecture is:

```text
                         Users
                           │
                           ▼
                     HTTPS / TLS
                           │
                           ▼
                  Reverse Proxy / Nginx
                           │
                           ▼
                 FastAPI Application
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          Employee Routes       Manager Routes
                │                     │
                └──────────┬──────────┘
                           │
                           ▼
                      Service Layer
                           │
                           ▼
                     Repository Layer
                           │
                           ▼
                  PostgreSQL Database
                           │
                           ▼
                    Backup Storage
```

For a small internal application, SQLite can continue to be used initially.

If the number of concurrent users or submissions increases, the recommended migration path is:

```text
SQLite
  │
  │ Scale requirements increase
  ▼
PostgreSQL
```

---

# 40. Recommended Deployment Lifecycle

The long-term deployment lifecycle should be:

```text
Developer
    │
    ▼
Git Repository
    │
    ▼
CI/CD Pipeline
    │
    ├── Run Tests
    │
    ├── Build Docker Image
    │
    ├── Tag Image
    │
    └── Deploy
          │
          ▼
    Production Environment
          │
          ├── FastAPI
          ├── Persistent Database
          ├── Backups
          └── Monitoring
```

---

# 41. Quick Reference

## Local Development

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\Activate.ps1
```

```powershell
python -m pip install -r requirements.txt
```

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Docker Build

```powershell
docker build -t mm-task-tracker .
```

---

## Docker Run

```powershell
docker run -p 8000:8000 mm-task-tracker
```

---

## Docker Compose

```powershell
docker compose up --build
```

Background mode:

```powershell
docker compose up --build -d
```

---

## View Logs

```powershell
docker compose logs -f
```

---

## Stop

```powershell
docker compose down
```

---

## Restart

```powershell
docker compose restart
```

---

# 42. Deployment Summary

The MM Task Tracker is currently designed as a lightweight FastAPI application with SQLite persistence.

The simplest deployment model is:

```text
Docker Compose
      │
      ▼
FastAPI + Uvicorn
      │
      ▼
SQLite
```

For development:

```text
Python Virtual Environment
      │
      ▼
Uvicorn --reload
      │
      ▼
SQLite
```

For production, the recommended next steps are to ensure database persistence, introduce a dedicated health endpoint, use validated request models, configure environment-specific settings, add authentication to manager functionality, and establish automated database backups.

The deployment architecture should evolve gradually as the application's user count, data volume, and reliability requirements increase.
