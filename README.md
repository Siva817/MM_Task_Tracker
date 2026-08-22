# MM Task Tracker

FastAPI-based web application for tracking employee tasks, employee status, manager information, and task visibility.

The application provides separate employee and manager dashboards and uses SQL Server/Azure SQL for persistent data storage.

## Features

### Employee Dashboard

* Employee ID and employee name entry
* Manager selection from the database
* MM dashboard/task parsing
* Task-level SWAY and MM status
* Jobs and remarks
* Idle status reporting
* Drive link and idle remarks
* Submission confirmation
* Submit-button loading indicator to prevent duplicate submissions

### Manager Dashboard

* Employee status summary
* Idle vs Production chart
* Task visibility chart
* Manager filtering
* Date filtering
* Latest employee submission table
* Idle employee table
* Employee/task visibility lookup
* Task status report
* CSV export for dashboard tables
* Timestamped CSV filenames for repeated downloads

## Technology Stack

| Component               | Technology                 |
| ----------------------- | -------------------------- |
| Backend                 | FastAPI                    |
| Web server - local      | Uvicorn                    |
| Web server - Azure      | Gunicorn + Uvicorn workers |
| Template engine         | Jinja2                     |
| Database                | SQL Server / Azure SQL     |
| Database ORM/connection | SQLAlchemy                 |
| SQL Server driver       | pyodbc                     |
| Dependency management   | uv                         |
| Configuration           | python-dotenv              |
| Frontend                | HTML, CSS, JavaScript      |
| Charts                  | Chart.js                   |
| Deployment              | Azure App Service          |
| CI/CD                   | GitHub Actions             |

## Project Structure

```text
MM_Task_Tracker/
│
├── app/
│   ├── data/
│   │   └── managers.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── ...
│   │
│   ├── models/
│   │   └── employee.py
│   │
│   ├── routers/
│   │   ├── employee.py
│   │   └── manager.py
│   │
│   ├── services/
│   │   ├── manager.py
│   │   ├── submission_service.py
│   │   └── dashboard_cache.py
│   │
│   ├── static/
│   │   ├── employee.js
│   │   ├── manager.js
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── employee.html
│   │   └── manager.html
│   │
│   └── main.py
│
├── .github/
│   └── workflows/
│       └── main_mm-task-tracker-test.yml
│
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── .env
└── README.md
```

> The exact project structure may change as the application develops.

## Requirements

* Python 3.12 or later
* `uv`
* SQL Server or Azure SQL Database
* Microsoft ODBC Driver 18 for SQL Server
* Git

For Azure deployment, the App Service environment provides the Linux runtime used by Gunicorn.

## Dependency Management with uv

The project uses `uv` for dependency management.

Install dependencies:

```powershell
uv sync
```

Update the lock file after changing dependencies:

```powershell
uv lock
```

Run a Python command through the project environment:

```powershell
uv run python --version
```

The project keeps `uv.lock` under source control so dependency versions are reproducible.

## Local Development

Start the FastAPI application locally with Uvicorn:

```powershell
uv run uvicorn app.main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```
Employee form submit page:

```text
http://127.0.0.1:8000/employee/page
```
Manager Dashboard:

```text
http://127.0.0.1:8000/manager
```

## Environment Variables

Create a `.env` file for local development.

Example:

```env
SQL_SERVER=your-server.database.windows.net
SQL_DATABASE=your-database
SQL_USERNAME=your-username
SQL_PASSWORD=your-password
```

Do not commit `.env` or database credentials to Git.

The application uses:

```python
load_dotenv()
```

to load environment variables.

## Database

The application uses SQL Server/Azure SQL through SQLAlchemy and `pyodbc`.

The SQLAlchemy connection uses:

```text
mssql+pyodbc
```

with:

```text
ODBC Driver 18 for SQL Server
```

The database currently contains tables including:

* `managers`
* `submissions`
* `tasks`

The relationship between submissions and tasks is:

```text
submissions
    │
    │ 1
    │
    └──────────< tasks
                 *
```

`tasks.submission_id` references `submissions.id`.

## Manager Data

Manager names are maintained in:

```text
app/data/managers.py
```

The application seeds the manager list into the `managers` table.

The manager dropdown on the employee page retrieves the manager list from the database.

## Running Locally

Typical development workflow:

```powershell
uv sync
uv run uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Production Deployment

The application is deployed to Azure App Service.

### Local development server

Uvicorn is used during development:

```text
uv run uvicorn app.main:app --reload
```

### Azure production server

Azure App Service uses Gunicorn with Uvicorn workers:

```text
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Explanation:

* `app.main:app` — FastAPI application object
* `-w 4` — starts four worker processes
* `-k uvicorn.workers.UvicornWorker` — uses Uvicorn workers for the ASGI application
* `-b 0.0.0.0:8000` — binds the application to port 8000

Gunicorn is intended for the Linux Azure environment. It is not used as the local Windows development server.

## Dependency Files

The project maintains:

### `pyproject.toml`

Contains the project's dependency definitions and metadata.

### `uv.lock`

Contains the locked dependency versions used by `uv`.

### `requirements.txt`

Used by the Azure GitHub Actions deployment workflow:

```text
pip install -r requirements.txt
```

When dependencies change, update the lock file and regenerate the requirements file as needed.

## CI/CD

The project uses GitHub Actions for Azure deployment.

The general deployment flow is:

```text
Git push
   ↓
GitHub Actions
   ↓
Azure authentication
   ↓
Install Python dependencies
   ↓
Deploy application
   ↓
Azure App Service
```

The GitHub Actions workflow is located under:

```text
.github/workflows/
```

## Important Production Dependencies

The project uses:

```text
FastAPI
Uvicorn
Gunicorn
SQLAlchemy
pyodbc
Jinja2
Pydantic
python-dotenv
```

`mssql-python` is not used by the current SQL Server connection.

The application connects through:

```text
SQLAlchemy → pyodbc → ODBC Driver 18 → SQL Server/Azure SQL
```

## Security

Never commit:

* `.env`
* Database passwords
* Access tokens
* Refresh tokens
* Client secrets
* Azure credentials

Use environment variables or Azure App Service configuration for production secrets.

## Development Notes

### Uvicorn vs Gunicorn

Uvicorn is convenient for local development:

```text
uvicorn app.main:app --reload
```

Gunicorn is used for the Azure production environment:

```text
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

Gunicorn should not be tested directly on Windows because it depends on Unix-specific functionality such as Python's `fcntl` module.

## Current Architecture

```text
                    ┌─────────────────────┐
                    │    Employee User    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │                     │
                    │ Employee / Manager  │
                    │      Routers        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
      ┌─────────────────┐              ┌─────────────────┐
      │     Services    │              │     Jinja2      │
      │                 │              │    Templates    │
      └────────┬────────┘              └─────────────────┘
               │
               ▼
      ┌─────────────────┐
      │    SQLAlchemy   │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │     pyodbc      │
      └────────┬────────┘
               │
               ▼
      ┌─────────────────┐
      │ SQL Server /    │
      │    Azure SQL    │
      └─────────────────┘
```

## Future Improvements

Potential future improvements include:

* Further optimization of Manager Dashboard database queries
* Server-side pagination for large employee tables
* Lazy loading of employee and idle tables
* Improved dashboard caching
* Database indexing optimization
* Gunicorn worker tuning based on Azure App Service resources
* More comprehensive application logging
* Automated tests
* Improved error handling and user notifications

## License

Internal project.
