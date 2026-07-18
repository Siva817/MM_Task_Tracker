# MM Task Tracker

## Overview

MM Task Tracker is a FastAPI-based web application that allows employees to submit their current MM task status and enables managers to consolidate team information.

The application helps capture:

* Employee details
* Manager name
* Current working task
* SWAY assessment status
* MM assessment status
* Job availability
* Remarks
* Idle status with Drive folder link and remarks

---

## Current Features

### Employee Page

* Enter Employee ID and Employee Name
* Select Manager from a dropdown
* Paste MM Dashboard
* Automatically parse available tasks
* Select the current task
* Mark:

  * SWAY Cleared
  * MM Cleared
  * Jobs Available / Jobs Not Available / Error
* Add remarks for each task
* Select **Idle** when not working
* Add Drive folder link and idle remarks
* Submit data to the FastAPI backend

---

## Technology Stack

* Python 3.12+
* FastAPI
* Uvicorn
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
│   ├── models/
│   │   ├── employee.py
│   │   └── enum.py
│   ├── routes/
│   │   ├── employee.py
│   │   └── manager.py
│   ├── services/
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── employee.html
│
├── docs/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Siva817/MM_Task_Tracker.git
```

Move into the project folder:

```bash
cd MM_Task_Tracker
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
```

Activate it:

### Command Prompt

```bash
.venv\Scripts\activate
```

### PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Git Bash

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the application in your browser:

```
http://127.0.0.1:8000/employee/page
```

---

## Development Workflow

After making changes:

```bash
git status
git add .
git commit -m "Describe your changes"
git push
```

To get the latest updates from GitHub:

```bash
git pull
```

---

## Current Status

Completed:

* Employee submission page
* MM dashboard parser
* Manager dropdown
* Idle workflow
* Frontend to backend communication
* JSON submission to FastAPI

Planned:

* SQLite database
* Manager dashboard
* Data consolidation
* Employee history
* Reports and analytics

---

## Author

Shiva Prasad
