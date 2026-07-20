# MM Task Tracker

A FastAPI-based web application for tracking employee task status, idle events, and task-related information. Employee submissions are stored in a SQLite database and can later be viewed through a manager dashboard.

---

## Features

### Employee Portal

* Submit employee ID and employee name
* Select manager
* Paste MM Dashboard and automatically parse tasks
* Select the current working task
* Mark SWAY and MM clearance status
* Record job availability
* Add task remarks
* Submit Idle events with:

  * Drive file/folder link
  * Idle remarks

### Backend

* FastAPI REST API
* SQLite database
* Stores employee submissions
* Stores parsed tasks linked to each submission
* Automatic submission timestamp

---

## Tech Stack

* Python 3
* FastAPI
* SQLite
* HTML
* CSS
* JavaScript

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
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd MM_Task_Tracker
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Initialize the Database

Run:

```bash
python -m app.db.init_db
```

This creates the SQLite database and required tables.

---

## Run the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

Application metadata:

* **Title:** MM Task Tracker
* **Description:** A FastAPI application to track employee tasks and events.
* **Version:** 1.0.0

---

## Database

SQLite is used as the local database.

Current tables:

* `submissions`
* `tasks`

Each submission can contain multiple tasks through a foreign key relationship.

---

## Current Status

Completed:

* Employee submission page
* MM Dashboard task parser
* Idle workflow
* SQLite persistence
* Task storage
* Timestamp recording

Planned:

* Manager dashboard
* Submission history
* Search and filtering
* Reports and analytics

## Author

Shiva Prasad