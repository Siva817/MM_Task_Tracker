# MM Task Tracker

A FastAPI-based web application for tracking employee task status, idle events, and task-related information. Employee submissions are stored in a SQLite database and can be viewed and analyzed through the Manager Dashboard.

The application can be run in two ways:

1. **Locally with Python and Uvicorn** — recommended for development
2. **With Docker** — recommended for containerized deployment and testing

---

## Features

### Employee Portal

* Submit employee ID and employee name
* Employee IDs and employee names are normalized when saved
* Select manager
* Paste MM Dashboard data and automatically parse tasks
* Select the current working task
* Mark SWAY and MM clearance status
* Record job availability:

  * Not Checked
  * Jobs Available
  * Jobs Not Available
  * Error / Can't Work
* Add task remarks
* Submit Idle events with:

  * Drive file/folder link
  * Idle remarks

### Manager Dashboard

* View employee status summary:

  * Idle employees
  * Production employees
  * Total employees
* Idle vs Production doughnut chart
* Task visibility employee count chart
* Manager filter
* Date filter
* Employee current-task table
* Task visibility lookup by:

  * Employee ID
  * Task ID
* Task status report:

  * Not Checked
  * Jobs Available
  * Jobs Not Available
  * Error / Can't Work
* Idle employees table with:

  * Employee ID
  * Employee name
  * Manager
  * Drive link
  * Idle remarks
  * Last log time
* Show/hide controls for dashboard tables
* CSV export buttons for four Manager Dashboard tables

### Backend

* FastAPI REST API
* SQLite database
* Stores employee submissions
* Stores parsed tasks linked to each submission
* Automatic submission timestamp
* Manager and date-based filtering
* Task visibility reporting
* Task status reporting
* Idle employee reporting

---

## Tech Stack

* Python 3
* FastAPI
* Uvicorn
* SQLite
* HTML
* CSS
* JavaScript
* Chart.js
* Docker
* Docker Compose

---

## Project Structure

```text
MM_Task_Tracker/
│
├── app/
│   ├── main.py
│   ├── db/
│   │   ├── database.py
│   │   ├── init_db.py
│   │   └── tracker.db
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
│
├── docs/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd MM_Task_Tracker
```

---

# Option 1: Run Locally with Uvicorn

Running with Uvicorn is recommended during development because code changes can be tested quickly with `--reload`.

## 1. Create a Virtual Environment

```bash
python -m venv .venv
```

## 2. Activate the Virtual Environment

### Windows

```bash
source .venv/Scripts/activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Initialize the Database

The application uses SQLite.

The database file is located at:

```text
app/db/tracker.db
```

To initialize the database and create the required tables, run:

```bash
python -m app.db.init_db
```

If the database already exists and contains data, do not delete or recreate it unless you intentionally want to reset the database.

---

## 5. Run the Application with Uvicorn

Start the development server:

```bash
uvicorn app.main:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

The application provides the following pages:

MM Task Tracker Employee Form: http://127.0.0.1:8000/employee/page
Manager Dashboard: http://127.0.0.1:8000/manager

---

## Option 2: Run with Docker

Docker runs the application using the Python environment defined inside the Docker image.

You do not need to activate the local `.venv` to run the Docker container.

### Build the Docker Image

From the project root:

```bash
docker build -t mm-task-tracker .
```

Check that the image was created:

```bash
docker images
```

You should see:

```text
mm-task-tracker
```

### Run the Docker Container

The SQLite database is located at:

```text
app/db/tracker.db
```

To make sure database changes persist outside the Docker container, mount the local `app/db` directory into the container.

### Git Bash

```bash
docker run -p 8000:8000 -v "$(pwd)/app/db:/app/app/db" mm-task-tracker
```

### PowerShell

```powershell
docker run -p 8000:8000 `
    -v "${PWD}/app/db:/app/app/db" `
    mm-task-tracker
```

The application will then be available at:

```text
http://localhost:8000
```

The database remains stored locally at:

```text
app/db/tracker.db
```

This means removing the Docker container does not remove the database stored on the host machine.

---

# Option 3: Run with Docker Compose

Docker Compose provides an easier way to build and run the application with the SQLite database volume configured automatically.

The project contains:

```text
docker-compose.yml
```

Start the application:

```bash
docker compose up --build
```

The application will be available at:

```text
http://localhost:8000
```
The application provides the following pages:

MM Task Tracker Employee Form: http://localhost:8000/employee/page
Manager Dashboard: http://localhost:8000/manager

To stop the application:

```bash
docker compose down
```

The SQLite database remains at:

```text
app/db/tracker.db
```

because the database directory is mounted as a Docker volume.

---

# Choosing How to Run the Application

## Development

Use Uvicorn:

```bash
uvicorn app.main:app --reload
```

This is the recommended approach while actively developing the application.

## Docker Testing or Deployment

Use Docker:

```bash
docker compose up --build
```

This runs the application inside a container and uses the Docker configuration defined by the project.

---

# Important: Do Not Run Both on Port 8000

The Uvicorn and Docker versions cannot both use port `8000` at the same time.

For example, if Uvicorn is running:

```text
http://localhost:8000
```

stop it before starting Docker.

Stop Uvicorn with:

```text
Ctrl + C
```

Then start Docker.

Alternatively, Docker can be mapped to another host port:

```bash
docker run -p 8001:8000 -v "$(pwd)/app/db:/app/app/db" mm-task-tracker
```

Then:

```text
Uvicorn → http://localhost:8000
Docker  → http://localhost:8001
```

The first port is the host port, while the second port is the container port.

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

When running through Docker, the same endpoints are available through:

```text
http://localhost:8000/docs
```

Application metadata:

* **Title:** MM Task Tracker
* **Description:** A FastAPI application to track employee tasks and events.
* **Version:** 1.0.0

---

# Database

SQLite is used as the local database.

Database file:

```text
app/db/tracker.db
```

Current tables include:

* `submissions`
* `tasks`

Each submission can contain multiple tasks through a foreign key relationship.

The database is shared between the local Uvicorn and Docker workflows when Docker is run with the `app/db` volume mapping.

---

# CSV Export

The Manager Dashboard provides CSV export buttons for four dashboard tables.

The exported CSV files contain the current table data displayed in the dashboard at the time of export.

CSV exports are generated from the table data currently available in the browser.

---

# Current Status

Completed:

* Employee submission page
* Employee ID and employee name normalization
* MM Dashboard task parser
* Idle workflow
* SQLite persistence
* Task storage
* Timestamp recording
* Manager Dashboard
* Manager filtering
* Date filtering
* Employee status summary cards
* Idle vs Production doughnut chart
* Task visibility chart
* Current task employee table
* Task visibility lookup
* Task status report
* Idle employees report
* Show/hide dashboard tables
* CSV export for four Manager Dashboard tables
* Local Uvicorn execution
* Docker support
* Docker Compose support
* Persistent SQLite database volume for Docker

---

## Author

Shiva Prasad Akamgari
