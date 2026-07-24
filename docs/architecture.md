# MM Task Tracker — System Architecture

## 1. Document Purpose

This document describes the architecture of the **MM Task Tracker** application.

The purpose of this document is to:

* Explain how the current system is structured.
* Define the responsibilities of each application layer.
* Document how data flows through the system.
* Establish conventions for future development.
* Prevent business logic from becoming tightly coupled to routes or frontend code.
* Provide a reference for developers working on the project in the future.
* Define a path for scaling the application as new features are added.

This document should be treated as a **living architecture document** and updated whenever significant architectural changes are introduced.

---

# 2. System Overview

MM Task Tracker is a web-based task tracking and assessment application.

The system provides separate workflows for:

* Employees
* Managers

The employee workflow allows users to:

1. Enter or parse task-related information.
2. Select or provide manager information.
3. Review the tasks identified by the system.
4. Provide task assessment information.
5. Handle special task states such as idle tasks.
6. Submit completed task data.

The manager workflow allows managers to:

1. View employee submissions.
2. Review task information.
3. Search and filter records.
4. View dashboard statistics.
5. Inspect task and employee data.
6. Export data to CSV.

The application is designed as a layered web application:

```text
                    ┌─────────────────────────┐
                    │       User / Browser    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ HTML / CSS / JavaScript │
                    │                         │
                    │ employee.html           │
                    │ manager.html            │
                    │ script.js               │
                    │ manager.js              │
                    │ style.css               │
                    └────────────┬────────────┘
                                 │
                          HTTP / API Requests
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       FastAPI App       │
                    │        main.py          │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
                ▼                                 ▼
       ┌──────────────────┐              ┌──────────────────┐
       │      Routes      │              │      Static /    │
       │                  │              │    Templates     │
       │ employee.py      │              │                  │
       │ manager.py       │              │ HTML / JS / CSS  │
       └────────┬─────────┘              └──────────────────┘
                │
                ▼
       ┌──────────────────┐
       │     Services     │
       │                  │
       │ manager.py       │
       │ submission_      │
       │ service.py       │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │      Models      │
       │                  │
       │ employee.py      │
       │ enum.py          │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │    Database      │
       │                  │
       │ database.py      │
       │ tracker.db       │
       │ init_db.py       │
       └──────────────────┘
```

---

# 3. Technology Stack

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic / FastAPI models
* SQLite

## Frontend

* HTML
* CSS
* JavaScript
* Fetch API

## Database

* SQLite
* `tracker.db`

## Containerization

* Docker
* Docker Compose

## Dependency Management

* `requirements.txt`

---

# 4. Project Structure

Current project structure:

```text
D:.
│   .dockerignore
│   .gitignore
│   docker-compose.yml
│   Dockerfile
│   README.md
│   requirements.txt
│
└───app
    │   main.py
    │
    ├───data
    │       managers.py
    │
    ├───db
    │       database.py
    │       init_db.py
    │       tracker.db
    │
    ├───models
    │       employee.py
    │       enum.py
    │
    ├───routes
    │       employee.py
    │       manager.py
    │
    ├───services
    │       manager.py
    │       submission_service.py
    │
    ├───static
    │       manager.js
    │       script.js
    │       style.css
    │
    └───templates
            employee.html
            manager.html
```

The project follows a simplified layered architecture.

```text
app
│
├── main.py
│       Application entry point
│
├── data
│       Static/reference data
│
├── db
│       Database configuration and initialization
│
├── models
│       Data models and enums
│
├── routes
│       HTTP/API layer
│
├── services
│       Business logic
│
├── static
│       Frontend JavaScript and CSS
│
└── templates
        HTML pages
```

---

# 5. Architectural Layers

The application is divided into the following logical layers:

```text
Presentation Layer
        │
        ▼
Routing / API Layer
        │
        ▼
Service / Business Logic Layer
        │
        ▼
Model Layer
        │
        ▼
Data Access / Database Layer
```

Each layer should have a clearly defined responsibility.

---

# 6. Application Entry Point

## `app/main.py`

`main.py` is the main entry point of the FastAPI application.

Responsibilities include:

* Creating the FastAPI application.
* Registering routers.
* Configuring application-level middleware if required.
* Mounting static files.
* Configuring template handling.
* Defining application startup behavior where required.

Conceptually:

```text
main.py
   │
   ├── Create FastAPI application
   │
   ├── Register employee routes
   │
   ├── Register manager routes
   │
   ├── Mount static files
   │
   └── Configure templates
```

`main.py` should remain lightweight.

Business logic should not be implemented directly inside `main.py`.

---

# 7. Routes Layer

Location:

```text
app/routes/
```

Current files:

```text
employee.py
manager.py
```

The routes layer is responsible for handling HTTP requests.

It acts as the interface between the frontend and the backend application.

## Employee Routes

`routes/employee.py`

Responsible for employee-facing endpoints.

Examples of responsibilities:

* Receiving employee submissions.
* Receiving task data.
* Processing employee requests.
* Returning employee-related information.
* Calling appropriate services.

## Manager Routes

`routes/manager.py`

Responsible for manager-facing endpoints.

Examples of responsibilities:

* Retrieving manager dashboard data.
* Retrieving employee submissions.
* Searching records.
* Filtering records.
* Returning lookup results.
* Supporting CSV export functionality.

Routes should remain relatively thin.

Preferred flow:

```text
HTTP Request
     │
     ▼
Route
     │
     ▼
Validate Input
     │
     ▼
Call Service
     │
     ▼
Receive Result
     │
     ▼
Return HTTP Response
```

The route should not contain complex business rules.

---

# 8. Services Layer

Location:

```text
app/services/
```

Current files:

```text
manager.py
submission_service.py
```

The service layer contains business logic.

This layer is the core of the application's backend behavior.

## `services/submission_service.py`

Responsible for submission-related business logic.

Potential responsibilities include:

* Processing employee submissions.
* Validating submission data.
* Applying business rules.
* Handling task assessment data.
* Managing special task states.
* Preparing data for database persistence.

The submission service should be the primary location for rules concerning the employee submission workflow.

Example:

```text
Employee
   │
   ▼
Employee Frontend
   │
   ▼
Employee Route
   │
   ▼
Submission Service
   │
   ├── Validate data
   ├── Apply business rules
   ├── Process task information
   └── Save submission
   │
   ▼
Database
```

## `services/manager.py`

Responsible for manager-related business logic.

Potential responsibilities include:

* Retrieving manager dashboard data.
* Filtering employee submissions.
* Searching task records.
* Preparing lookup results.
* Aggregating dashboard statistics.

The manager service should contain manager-specific business rules rather than placing them directly in `routes/manager.py`.

---

# 9. Models Layer

Location:

```text
app/models/
```

Current files:

```text
employee.py
enum.py
```

The models layer defines the structure and allowed values of application data.

## `models/employee.py`

Responsible for employee-related data structures.

Depending on implementation, this may contain:

* Employee request models.
* Employee response models.
* Submission models.
* Validation models.

The model layer should define the shape of data exchanged between the frontend and backend.

## `models/enum.py`

Contains enumerated values used throughout the application.

Examples may include task statuses or assessment states.

Enums should be used when a field has a predefined set of valid values.

For example:

```text
Task Status
    ├── Completed
    ├── Idle
    └── Error

Assessment
    ├── Dry
    ├── Flow
    ├── Not Working
    └── Error
```

The actual enum values should remain centralized rather than duplicated across multiple files.

This prevents inconsistent values between:

* Frontend
* Backend
* Database
* Reports

---

# 10. Database Layer

Location:

```text
app/db/
```

Current files:

```text
database.py
init_db.py
tracker.db
```

## `database.py`

Responsible for database connectivity and database configuration.

Responsibilities should include:

* Creating database connections.
* Managing database sessions or connections.
* Providing database access to services.
* Managing connection lifecycle.

Database-specific logic should remain isolated from routes.

## `init_db.py`

Responsible for database initialization.

It should be used to:

* Create required tables.
* Initialize the database schema.
* Perform initial database setup.

Database initialization should be repeatable and predictable.

## `tracker.db`

SQLite database containing application data.

The database should not be treated as application logic.

The application should access the database through the database layer rather than directly from frontend code.

---

# 11. Data Layer

Location:

```text
app/data/
```

Current file:

```text
managers.py
```

This directory contains static or reference data used by the application.

`managers.py` currently represents manager-related reference data.

The data layer should be used for data that is not necessarily part of the transactional database workflow.

For example:

```text
Reference Data
    │
    ├── Manager names
    ├── Static configuration
    └── Other controlled lists
```

## Future Direction

As the application grows, manager information should preferably move from hardcoded Python data into the database if managers become dynamic entities.

Future architecture:

```text
Current:

managers.py
    │
    ▼
Static Manager List


Future:

Manager Database Table
    │
    ▼
Manager Service
    │
    ▼
Manager Routes
```

This will allow managers to be:

* Added dynamically.
* Updated.
* Deactivated.
* Associated with employees.
* Used for authentication and authorization.

---

# 12. Frontend Architecture

Location:

```text
app/templates/
app/static/
```

The frontend currently consists of two main pages.

```text
templates/
├── employee.html
└── manager.html

static/
├── script.js
├── manager.js
└── style.css
```

---

## Employee Frontend

### `templates/employee.html`

Provides the employee-facing interface.

The employee interface is responsible for:

* Accepting task-related input.
* Displaying parsed tasks.
* Allowing task assessment.
* Handling task states.
* Collecting submission data.
* Sending data to backend APIs.

### `static/script.js`

Contains employee-side JavaScript.

Responsibilities may include:

* Form handling.
* API requests.
* Dynamic task rendering.
* Validation.
* Toggle interactions.
* Submission behavior.
* Idle task handling.

The employee frontend should communicate with the backend through APIs.

```text
employee.html
      │
      ▼
script.js
      │
      │ HTTP Request
      ▼
Employee API
```

---

## Manager Frontend

### `templates/manager.html`

Provides the manager dashboard interface.

Responsibilities include:

* Displaying dashboard cards.
* Displaying charts.
* Showing employee/task data.
* Providing filters.
* Showing and hiding tables.
* Providing search and lookup functionality.
* Providing CSV export functionality.

### `static/manager.js`

Contains manager dashboard JavaScript.

Responsibilities may include:

* Fetching manager data.
* Updating dashboard cards.
* Rendering charts.
* Applying filters.
* Managing table visibility.
* Exporting data to CSV.
* Handling lookup results.

The manager dashboard should remain primarily a presentation layer.

Business rules should be implemented on the backend where appropriate.

---

# 13. Frontend to Backend Communication

The application uses HTTP APIs to communicate between frontend and backend.

General flow:

```text
User Action
    │
    ▼
JavaScript Event Handler
    │
    ▼
Fetch API Request
    │
    ▼
FastAPI Route
    │
    ▼
Service Layer
    │
    ▼
Database
    │
    ▼
Service Response
    │
    ▼
FastAPI Response
    │
    ▼
JavaScript
    │
    ▼
Update UI
```

The frontend should not directly access the SQLite database.

---

# 14. Employee Submission Flow

The expected employee submission flow is:

```text
Employee Opens Application
        │
        ▼
Enter / Parse Task Information
        │
        ▼
Select Manager
        │
        ▼
Validate Manager
        │
        ▼
Parse Tasks
        │
        ▼
Display Number of Tasks Found
        │
        ▼
Display Task List
        │
        ▼
Employee Provides Assessment
        │
        ├── Dry
        ├── Flow
        ├── Not Working
        └── Error
        │
        ▼
Handle Idle Tasks
        │
        ├── Driver File / Folder Link
        └── Remarks
        │
        ▼
Validate Submission
        │
        ▼
Submit
        │
        ▼
Store in Database
```

---

# 15. Manager Validation

Manager validation is an important business rule.

The application should distinguish between:

```text
Parse
    │
    └── May be possible without manager

Submit
    │
    └── Requires valid manager
```

The architecture should preserve this distinction.

The frontend may provide immediate validation feedback, but the backend must remain the authoritative validation layer.

The backend should never trust manager information supplied by the browser without validation.

---

# 16. Task Assessment Architecture

Task assessment values should be standardized.

Instead of allowing arbitrary text values, the system should use predefined enums wherever possible.

Example:

```text
Task
  │
  ├── Assessment
  │      ├── Dry
  │      ├── Flow
  │      ├── Not Working
  │      └── Error
  │
  └── Status
         ├── Active
         └── Idle
```

Invalid values should be rejected or clearly handled.

If a user enters an invalid or unsupported value, the frontend should provide guidance instead of silently accepting incorrect data.

Backend validation must also be applied.

---

# 17. Idle Task Architecture

Idle tasks are treated differently from normal active tasks.

When a task is marked as idle, additional information may become available or required.

For example:

```text
Idle Task
    │
    ├── Driver File / Folder Link
    │
    └── Remarks
```

These fields should remain hidden or inactive until the user selects the idle state.

Frontend behavior:

```text
Task is not Idle
    │
    └── Hide idle-specific fields


Task is Idle
    │
    └── Show idle-specific fields
```

The backend should still validate the submitted data.

Frontend visibility should not be considered sufficient validation.

---

# 18. Manager Dashboard Architecture

The manager dashboard consists of several presentation components.

Conceptually:

```text
Manager Dashboard
        │
        ├── Filters
        │
        ├── Summary Cards
        │
        ├── Doughnut Chart
        │
        ├── Additional Charts
        │
        ├── Data Tables
        │
        └── Lookup Results
```

The dashboard should retrieve data from backend APIs.

The frontend should be responsible for:

* Rendering.
* Filtering displayed data.
* User interactions.
* Chart updates.

The backend should be responsible for:

* Data retrieval.
* Business rules.
* Database filtering where appropriate.
* Aggregation of large datasets.

---

# 19. CSV Export Architecture

The manager dashboard provides CSV export functionality.

CSV export may be implemented in two ways.

## Client-Side Export

```text
Backend
    │
    ▼
JSON Data
    │
    ▼
Browser
    │
    ▼
JavaScript
    │
    ▼
Generate CSV
    │
    ▼
Download
```

This is appropriate for data already loaded into the browser.

## Server-Side Export

For larger datasets, the preferred future architecture is:

```text
Manager
    │
    ▼
Export Request
    │
    ▼
FastAPI Route
    │
    ▼
Manager Service
    │
    ▼
Database Query
    │
    ▼
CSV Generation
    │
    ▼
File Response
    │
    ▼
Browser Download
```

Server-side export is preferred when:

* The dataset is large.
* The export must exactly match database results.
* Filtering needs to happen server-side.
* Export logic becomes complex.

---

# 20. Error Handling

Errors should be handled at multiple levels.

## Frontend

The frontend should:

* Display clear validation messages.
* Prevent obviously invalid submissions.
* Handle failed API requests.
* Inform the user when an operation fails.

## Backend

The backend should:

* Validate all incoming data.
* Return appropriate HTTP status codes.
* Avoid exposing internal implementation details.
* Log unexpected exceptions.

General flow:

```text
Invalid User Input
      │
      ▼
Frontend Validation
      │
      ▼
User Correction


Invalid API Request
      │
      ▼
Backend Validation
      │
      ▼
4xx Response


Unexpected Server Error
      │
      ▼
Backend Logging
      │
      ▼
5xx Response
```

---

# 21. Security Architecture

The current application should be developed with the assumption that all client-side input is untrusted.

Important principles:

* Validate input on the backend.
* Do not trust manager values sent by the browser.
* Do not expose database files through static file serving.
* Do not store secrets in source code.
* Use environment variables for configuration.
* Validate URLs submitted as driver file or folder links.
* Avoid returning database internals to the frontend.

Future authentication should be implemented before the application is exposed broadly.

---

# 22. Configuration Management

Configuration should eventually be separated from application code.

Future structure:

```text
app/
├── config/
│   └── settings.py
```

Configuration should include:

* Database URL.
* Environment name.
* Debug mode.
* Application host.
* Application port.
* Authentication configuration.
* Other environment-specific settings.

Environment-specific values should be stored in environment variables.

Example:

```text
DATABASE_URL
APP_ENV
DEBUG
```

Secrets must not be committed to Git.

---

# 23. Docker Architecture

The project contains:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

The application is designed to run in a containerized environment.

Conceptually:

```text
Docker Compose
      │
      ▼
Application Container
      │
      ▼
FastAPI
      │
      ▼
SQLite
```

For the current architecture, SQLite is suitable for lightweight usage.

However, the database strategy should be reconsidered if the application becomes multi-user and heavily concurrent.

Future architecture may use:

```text
FastAPI Container
       │
       ▼
PostgreSQL Container / Managed PostgreSQL
```

This would provide better support for:

* Concurrent users.
* Transactions.
* Larger datasets.
* Production workloads.
* Database backups.

---

# 24. Database Evolution

The current application uses SQLite:

```text
tracker.db
```

SQLite is appropriate for:

* Development.
* Prototyping.
* Small deployments.
* Low-concurrency applications.

As the application grows, the database should be migrated to PostgreSQL or another production-grade relational database.

The migration should be made easier by ensuring that application code accesses the database through a dedicated database/data-access layer.

The business logic should not depend directly on SQLite-specific implementation details.

---

# 25. Recommended Future Project Structure

As the application grows, the following structure is recommended:

```text
app/
│
├── main.py
│
├── config/
│   └── settings.py
│
├── db/
│   ├── database.py
│   ├── init_db.py
│   └── migrations/
│
├── models/
│   ├── employee.py
│   ├── manager.py
│   ├── submission.py
│   └── enum.py
│
├── schemas/
│   ├── employee.py
│   ├── manager.py
│   └── submission.py
│
├── routes/
│   ├── employee.py
│   ├── manager.py
│   └── health.py
│
├── services/
│   ├── employee_service.py
│   ├── manager_service.py
│   ├── submission_service.py
│   └── export_service.py
│
├── repositories/
│   ├── employee_repository.py
│   ├── manager_repository.py
│   └── submission_repository.py
│
├── data/
│   └── seed_data.py
│
├── templates/
│   ├── employee.html
│   └── manager.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        ├── employee.js
        └── manager.js
```

The current project does not need to adopt this structure immediately.

It should be introduced gradually as complexity increases.

---

# 26. Recommended Repository Layer

The current architecture has:

```text
Routes
   │
   ▼
Services
   │
   ▼
Database
```

As the application grows, introduce repositories:

```text
Routes
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
Database
```

The repository layer should be responsible for database operations.

Example:

```text
manager_service.py
        │
        ▼
manager_repository.py
        │
        ▼
Database
```

This separation allows business logic to remain independent from database implementation details.

---

# 27. API Design Principles

All new APIs should follow consistent conventions.

Recommended structure:

```text
/api/employees
/api/employees/{employee_id}

/api/managers
/api/managers/{manager_id}

/api/submissions
/api/submissions/{submission_id}

/api/tasks
/api/tasks/{task_id}
```

The exact API structure may evolve, but APIs should be organized around domain resources.

Avoid creating endpoints that mix unrelated responsibilities.

For example, instead of:

```text
/api/do-everything
```

prefer:

```text
/api/submissions
/api/submissions/{id}
/api/managers
/api/tasks
```

---

# 28. Testing Architecture

Future development should introduce automated tests.

Recommended structure:

```text
tests/
├── test_employee_routes.py
├── test_manager_routes.py
├── test_submission_service.py
├── test_manager_service.py
└── test_validation.py
```

Testing should occur at multiple levels.

## Unit Tests

Test individual business rules.

Examples:

* Manager validation.
* Task status validation.
* Idle task validation.

## API Tests

Test FastAPI endpoints.

Examples:

* Employee submission.
* Manager lookup.
* Dashboard data retrieval.

## Integration Tests

Test the complete flow:

```text
API
  │
  ▼
Service
  │
  ▼
Database
```

---

# 29. Logging and Observability

Future production deployments should include structured logging.

Important events to log include:

* Application startup.
* Application shutdown.
* API errors.
* Database errors.
* Failed submissions.
* Unexpected exceptions.

Sensitive information should never be written to logs.

Future architecture may introduce:

```text
Application
    │
    ▼
Structured Logs
    │
    ▼
Log Aggregation
```

---

# 30. Health Checks

A future health endpoint should be introduced.

Example:

```text
GET /health
```

The endpoint can verify that the application is running.

A deeper readiness check may verify database connectivity:

```text
GET /health/ready
```

This is useful for Docker and future deployment platforms.

---

# 31. Development Rules

Future developers should follow these rules.

### Rule 1: Keep Routes Thin

Routes should coordinate requests and responses.

Do not place complex business logic inside route functions.

### Rule 2: Put Business Logic in Services

Business rules belong in the service layer.

### Rule 3: Keep Database Access Isolated

Database-specific operations should remain in the database or repository layer.

### Rule 4: Validate on the Backend

Frontend validation improves user experience.

Backend validation protects data integrity.

Both are required.

### Rule 5: Centralize Enums

Do not duplicate allowed values across multiple files.

### Rule 6: Avoid Hardcoded Business Data

Static manager lists should eventually be replaced with database-backed entities.

### Rule 7: Keep Frontend Logic Modular

As JavaScript grows, split large files into smaller modules.

### Rule 8: Update This Document

Significant architectural changes must be reflected in `architecture.md`.

---

# 32. Future Authentication and Authorization

The current architecture should eventually support authentication.

Future flow:

```text
User
  │
  ▼
Login
  │
  ▼
Authentication
  │
  ▼
User Identity
  │
  ├──────────────┐
  ▼              ▼
Employee       Manager
  │              │
  ▼              ▼
Employee UI    Manager UI
```

Authorization should ensure that:

* Employees can access employee functionality.
* Managers can access manager functionality.
* Managers can only access authorized data.

Authentication should be implemented at the backend level.

Frontend route hiding alone is not sufficient security.

---

# 33. Future Scalability

The architecture should evolve in stages.

## Stage 1 — Current

```text
FastAPI
   │
   ├── Routes
   ├── Services
   ├── Models
   └── SQLite
```

## Stage 2 — Growing Application

```text
FastAPI
   │
   ├── Routes
   ├── Services
   ├── Repositories
   ├── Models
   └── PostgreSQL
```

## Stage 3 — Production Application

```text
Frontend
    │
    ▼
FastAPI
    │
    ├── Authentication
    ├── Authorization
    ├── Routes
    ├── Services
    ├── Repositories
    │
    ▼
PostgreSQL
```

Additional infrastructure may eventually include:

* Reverse proxy.
* Centralized logging.
* Monitoring.
* Automated backups.
* CI/CD.
* Background job processing.

These should only be introduced when actual requirements justify the added complexity.

---

# 34. Architectural Decision Summary

| Decision        | Current Approach    | Future Direction                   |
| --------------- | ------------------- | ---------------------------------- |
| Backend         | FastAPI             | Continue                           |
| Frontend        | HTML/CSS/JavaScript | Modular JavaScript                 |
| Database        | SQLite              | PostgreSQL for scale               |
| Business Logic  | Services            | Maintain service layer             |
| Database Access | Database layer      | Repository layer                   |
| Manager Data    | Python data file    | Database-backed managers           |
| Validation      | Frontend + Backend  | Strong backend validation          |
| CSV Export      | Frontend-oriented   | Dedicated export service if needed |
| Authentication  | Not yet implemented | Add authentication                 |
| Authorization   | Not yet implemented | Role-based authorization           |
| Deployment      | Docker              | Docker + production infrastructure |
| Testing         | To be expanded      | Unit + API + integration tests     |
| Configuration   | Basic               | Environment-based configuration    |

---

# 35. Future Development Roadmap

The recommended development sequence is:

### Phase 1 — Stabilize Current Application

* Keep route and service responsibilities clear.
* Centralize enums.
* Improve backend validation.
* Ensure database operations are consistent.
* Document all APIs.

### Phase 2 — Improve Data Architecture

* Introduce dedicated schemas.
* Introduce repositories.
* Move manager data into the database.
* Add database migrations.

### Phase 3 — Improve Reliability

* Add automated tests.
* Add structured logging.
* Add health checks.
* Improve error handling.

### Phase 4 — Improve Security

* Add authentication.
* Add role-based authorization.
* Secure manager dashboard access.
* Validate user permissions on every protected endpoint.

### Phase 5 — Production Scalability

* Migrate from SQLite to PostgreSQL.
* Add production database backups.
* Add monitoring.
* Add CI/CD.
* Improve container deployment.

---

# 36. Core Architectural Principle

The most important architectural principle for MM Task Tracker is:

> **Keep the frontend responsible for presentation and user interaction, keep routes responsible for HTTP communication, keep services responsible for business rules, and keep the database layer responsible for persistence.**

The desired dependency direction is:

```text
Frontend
    │
    ▼
Routes
    │
    ▼
Services
    │
    ▼
Repositories / Data Access
    │
    ▼
Database
```

Dependencies should flow downward.

The database should never depend on the frontend.

The frontend should never directly access the database.

Routes should not contain complex business logic.

Services should not depend on HTML or browser-specific behavior.

This separation will allow MM Task Tracker to grow from its current lightweight application into a more maintainable and scalable system without requiring a complete rewrite.
