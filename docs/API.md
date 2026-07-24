# MM Task Tracker — API Documentation

## 1. Overview

The MM Task Tracker backend is built using **FastAPI**.

The API provides functionality for:

* Employee submission
* Manager retrieval
* Employee page rendering
* Manager dashboard rendering
* Employee task lookup
* Task-based employee lookup
* Task status reporting
* Manager dashboard filtering
* Submission persistence

The application currently uses a layered architecture:

```text
Browser
   │
   ▼
FastAPI Routes
   │
   ├── Employee Routes
   │
   └── Manager Routes
   │
   ▼
Service Layer
   │
   ├── submission_service.py
   └── manager.py
   │
   ▼
Database Layer
   │
   └── SQLite (tracker.db)
```

---

# 2. API Route Organization

The API is divided into two primary route modules:

```text
app/routes/
├── employee.py
└── manager.py
```

## Employee Routes

Defined in:

```text
app/routes/employee.py
```

Current endpoints:

```text
GET  /
POST /submit
GET  /page
GET  /managers
```

## Manager Routes

Defined in:

```text
app/routes/manager.py
```

Current endpoints:

```text
GET /
GET /lookup
GET /task-status-report
```

The actual full URL depends on how the routers are registered in `app/main.py`.

For example, if `main.py` contains:

```python
app.include_router(employee_router, prefix="/employee")
app.include_router(manager_router, prefix="/manager")
```

then the actual URLs would be:

```text
/employee/
/employee/submit
/employee/page
/employee/managers

/manager/
/manager/lookup
/manager/task-status-report
```

This document describes the route paths defined inside each router.

---

# 3. Employee API

The employee API manages the employee-facing workflow.

```text
Employee
   │
   ├── Open Employee Page
   │
   ├── Retrieve Managers
   │
   └── Submit Task Data
```

---

# 4. Employee Health Check

## `GET /`

### Purpose

Confirms that the employee router is working.

### Response

```json
{
    "message": "Employee Routes Working!"
}
```

### Example

```http
GET /
```

### Status Code

```text
200 OK
```

### Implementation

Defined in:

```text
app/routes/employee.py
```

Function:

```python
employee_home()
```

---

# 5. Employee Page

## `GET /page`

### Purpose

Renders the employee-facing HTML page.

### Response Type

```text
text/html
```

### Template

```text
app/templates/employee.html
```

### Example

```http
GET /page
```

### Response

The endpoint returns the rendered `employee.html` template.

### Implementation Flow

```text
Browser
   │
   │ GET /page
   ▼
employee_page()
   │
   ▼
Jinja2Templates
   │
   ▼
employee.html
   │
   ▼
HTML Response
```

### Implementation

```python
@router.get("/page", response_class=HTMLResponse)
def employee_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="employee.html",
        context={}
    )
```

---

# 6. Get Managers

## `GET /managers`

### Purpose

Returns the list of managers available in the database.

### Request

No request body is required.

### Example

```http
GET /managers
```

### Response

Returns a JSON array containing manager names.

Example:

```json
[
    "Manager One",
    "Manager Two",
    "Manager Three"
]
```

### Data Source

Managers are retrieved from the `managers` database table.

The query is:

```sql
SELECT name
FROM managers
ORDER BY name
```

### Implementation Flow

```text
GET /managers
       │
       ▼
employee.py
       │
       ▼
get_managers()
       │
       ▼
database.py
       │
       ▼
managers table
       │
       ▼
List[str]
```

### Service

```text
app/services/manager.py
```

Function:

```python
get_managers()
```

---

# 7. Employee Submission

## `POST /submit`

### Purpose

Accepts an employee submission and saves:

1. Submission-level information to the `submissions` table.
2. Task-level information to the `tasks` table.

### Request

The endpoint accepts a JSON request body.

The route currently reads the request manually:

```python
data = await request.json()
```

### Expected Request Structure

The current `save_submission()` implementation expects the following structure:

```json
{
    "employeeId": "EMP001",
    "employeeName": "John Doe",
    "manager": "Manager One",
    "currentTask": "Task A",
    "idle": false,
    "driveLink": "",
    "idleRemarks": "",
    "tasks": [
        {
            "id": "TASK001",
            "name": "Task One",
            "sway": true,
            "mm": false,
            "jobs": "Flow",
            "remarks": "Task remarks"
        },
        {
            "id": "TASK002",
            "name": "Task Two",
            "sway": false,
            "mm": true,
            "jobs": "Dry",
            "remarks": ""
        }
    ]
}
```

---

# 8. Submission Request Fields

## Submission-Level Fields

| Field          | Expected Type | Description                                  |
| -------------- | ------------- | -------------------------------------------- |
| `employeeId`   | String        | Employee identifier                          |
| `employeeName` | String        | Employee name                                |
| `manager`      | String        | Selected manager                             |
| `currentTask`  | String        | Employee's current task                      |
| `idle`         | Boolean       | Indicates whether employee is idle           |
| `driveLink`    | String        | Driver/file/folder link for idle information |
| `idleRemarks`  | String        | Remarks related to idle status               |
| `tasks`        | Array         | List of tasks associated with submission     |

---

## Task-Level Fields

Each object in the `tasks` array contains:

| Field     | Expected Type | Description               |
| --------- | ------------- | ------------------------- |
| `id`      | String        | Task identifier           |
| `name`    | String        | Task name                 |
| `sway`    | Boolean       | Sway status               |
| `mm`      | Boolean       | MM status                 |
| `jobs`    | String        | Job/task assessment value |
| `remarks` | String        | Task-specific remarks     |

---

# 9. Submission Database Flow

The submission is stored in two related tables.

```text
POST /submit
      │
      ▼
Request JSON
      │
      ▼
save_submission(data)
      │
      ├────────────────────────────┐
      │                            │
      ▼                            ▼
submissions table             tasks table
      │                            │
      │ submission ID              │
      └──────────────┬─────────────┘
                     │
                     ▼
               submission_id
```

The `submissions` table stores submission-level information.

The `tasks` table stores individual tasks belonging to that submission.

The relationship is:

```text
One Submission
      │
      ├── Task 1
      ├── Task 2
      ├── Task 3
      └── Task N
```

The `tasks.submission_id` field links each task to its parent submission.

---

# 10. Submission Data Transformation

The service performs several transformations before inserting data.

## Employee ID

Input:

```text
EMP001
```

Stored as:

```text
emp001
```

The code uses:

```python
data["employeeId"].strip().lower()
```

---

## Employee Name

Input:

```text
John Doe
```

Stored as:

```text
john doe
```

The code uses:

```python
data["employeeName"].strip().lower()
```

---

## Idle Boolean

Input:

```json
true
```

Stored in SQLite as:

```text
1
```

Input:

```json
false
```

Stored as:

```text
0
```

Implementation:

```python
1 if data["idle"] else 0
```

---

## Task Boolean Fields

The following fields are converted from Boolean to SQLite integer values:

```text
sway
mm
```

For example:

```json
"sway": true,
"mm": false
```

becomes:

```text
sway = 1
mm = 0
```

---

# 11. Submission Timestamp

The backend generates the submission timestamp.

The client does not provide the timestamp.

The service generates:

```python
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

Example:

```text
2026-07-24 00:30:45
```

This timestamp is stored in:

```text
submissions.submitted_at
```

This timestamp is used by manager dashboard queries for:

* Date filtering.
* Latest submission selection.
* Idle employee filtering.
* Task status reporting.

---

# 12. Submission Response

After the submission is saved successfully, the endpoint returns:

```json
{
    "message": "Data received successfully"
}
```

### Status Code

```text
200 OK
```

### Important Implementation Detail

The current route does not explicitly validate the submission before calling:

```python
save_submission(data)
```

It also does not explicitly validate:

* Manager existence.
* Required fields.
* Task structure.
* Task assessment values.
* Idle-specific fields.

The current `EmployeeSubmission` Pydantic model is imported but is **not currently used by the `/submit` endpoint**.

Therefore, the current API relies on the incoming JSON structure matching what `save_submission()` expects.

---

# 13. Submission Error Behavior

If the incoming JSON does not contain required keys, the service may raise a Python exception.

For example, missing:

```text
employeeId
```

may cause:

```python
KeyError
```

Similarly, missing:

```text
tasks
```

may cause an error when the service executes:

```python
for task in data["tasks"]:
```

Future versions should replace this behavior with explicit Pydantic validation.

Recommended architecture:

```text
POST /submit
     │
     ▼
EmployeeSubmission
     │
     ▼
Validated Data
     │
     ▼
save_submission()
```

---

# 14. Manager API

The manager API powers the manager dashboard.

The manager dashboard retrieves:

* All submissions.
* Latest submissions.
* Managers.
* Employee status counts.
* Task visibility.
* Idle employees.
* Task status reports.

The manager page also supports filtering by:

* Date.
* Manager.
* Task status.

---

# 15. Manager Dashboard

## `GET /`

### Purpose

Renders the manager dashboard.

### Query Parameters

| Parameter          | Type   | Optional | Description                     |
| ------------------ | ------ | -------- | ------------------------------- |
| `selected_date`    | String | Yes      | Filters data by submission date |
| `selected_manager` | String | Yes      | Filters data by manager         |
| `task_status`      | String | Yes      | Filters task status report      |

Example:

```http
GET /?selected_date=2026-07-24&selected_manager=Manager%20One&task_status=Flow
```

### Manager Dashboard Data

The endpoint retrieves:

```text
submissions
latest_submissions
managers
status_counts
task_visibility
idle_employees
task_status_report
```

The data is passed to:

```text
app/templates/manager.html
```

### Implementation Flow

```text
GET /
   │
   ├── get_all_submissions()
   │
   ├── get_latest_submissions()
   │
   ├── get_managers()
   │
   ├── get_employee_status_counts()
   │
   ├── get_task_visibility()
   │
   ├── get_idle_employees()
   │
   └── get_task_status_report()
          │
          ▼
     manager.html
```

---

# 16. Manager Dashboard Response

The endpoint returns HTML.

```text
Content-Type: text/html
```

The template receives the following context:

```python
{
    "request": request,
    "submissions": submissions,
    "latest_submissions": latest_submissions,
    "managers": managers,
    "status_counts": status_counts,
    "task_visibility": task_visibility,
    "selected_date": selected_date,
    "selected_manager": selected_manager,
    "idle_employees": idle_employees,
    "task_status_report": task_status_report
}
```

---

# 17. Get All Submissions

This operation is performed internally by the manager page.

### Service Function

```python
get_all_submissions()
```

### Database Query

The service retrieves:

```text
employee_id
employee_name
manager
current_task
idle
submitted_at
```

from:

```text
submissions
```

Results are ordered:

```text
submitted_at DESC
```

Therefore, the newest submissions appear first.

### Conceptual Data

```json
[
    {
        "employee_id": "emp001",
        "employee_name": "john doe",
        "manager": "Manager One",
        "current_task": "Task A",
        "idle": 0,
        "submitted_at": "2026-07-24 00:30:45"
    }
]
```

---

# 18. Latest Submissions

### Service Function

```python
get_latest_submissions(
    selected_date,
    selected_manager
)
```

### Purpose

Returns the latest submission for each employee.

### Query Parameters

```text
selected_date
selected_manager
```

### Filtering

If `selected_date` is provided:

```sql
DATE(submitted_at) = ?
```

If `selected_manager` is provided and is not `"All"`:

```sql
manager = ?
```

### Latest Submission Logic

The service uses:

```sql
MAX(id)
```

grouped by:

```text
employee_id
```

This means the latest record is determined by the highest submission ID.

### Important Note

The application currently assumes that a higher `id` represents a newer submission.

This works if IDs are generated sequentially and submissions are inserted normally.

---

# 19. Employee Status Counts

### Service Function

```python
get_employee_status_counts(
    selected_date,
    selected_manager
)
```

### Purpose

Counts employees based on their latest submission.

The result contains:

```json
{
    "total": 10,
    "idle": 3,
    "production": 7
}
```

### Calculation

```text
total = number of latest employee submissions

idle = submissions where idle = 1

production = total - idle
```

### Filters

Supports:

```text
selected_date
selected_manager
```

The manager filter is applied after retrieving the latest submissions.

---

# 20. Task Visibility

### Service Function

```python
get_task_visibility(
    selected_date,
    selected_manager
)
```

### Purpose

Determines how many employees are currently associated with each visible task.

### Returned Data

Conceptually:

```json
[
    {
        "task_id": "task001",
        "task_name": "Task One",
        "employee_count": 5
    }
]
```

### Filters

Supports:

```text
selected_date
selected_manager
```

### Database Logic

The query:

1. Finds the latest submission for each employee.
2. Joins those submissions with tasks.
3. Groups by task.
4. Counts distinct employees.

Results are ordered by:

```text
employee_count DESC
```

---

# 21. Idle Employees

### Service Function

```python
get_idle_employees(
    selected_date,
    selected_manager
)
```

### Purpose

Returns employees whose latest submission indicates that they are idle.

### Default Date

If no date is provided, the service defaults to today's date.

```python
datetime.now().strftime("%Y-%m-%d")
```

### Returned Fields

```text
employee_id
employee_name
manager
drive_link
idle_remarks
submitted_at
```

### Filtering

Supports:

```text
selected_date
selected_manager
```

### Idle Condition

Only records where:

```text
idle = 1
```

are returned.

---

# 22. Manager Lookup

## `GET /lookup`

### Purpose

Provides two lookup modes:

1. Employee lookup.
2. Task lookup.

The lookup mode is controlled using:

```text
lookup_type
```

---

# 23. Employee Lookup

### Request

```http
GET /lookup?lookup_type=employee&employee_id=EMP001
```

Optional manager filter:

```http
GET /lookup?lookup_type=employee&employee_id=EMP001&selected_manager=Manager%20One
```

### Parameters

| Parameter          | Type   | Required          | Description             |
| ------------------ | ------ | ----------------- | ----------------------- |
| `lookup_type`      | String | Yes               | Must be `employee`      |
| `employee_id`      | String | No at route level | Employee ID to search   |
| `selected_manager` | String | No                | Optional manager filter |

### Service

```python
get_employee_visible_tasks(
    employee_id,
    selected_manager
)
```

### Response

Returns an array of tasks visible for the employee.

Example:

```json
[
    {
        "employee_id": "emp001",
        "employee_name": "john doe",
        "manager": "Manager One",
        "submitted_at": "2026-07-24 00:30:45",
        "task_id": "task001",
        "task_name": "Task One",
        "jobs": "Flow",
        "remarks": "Task remarks"
    }
]
```

### Lookup Logic

The service:

1. Searches by employee ID.
2. Finds the latest submission for that employee.
3. Optionally filters by manager.
4. Returns tasks associated with that submission.

The employee ID comparison is case-insensitive:

```sql
LOWER(employee_id) = LOWER(?)
```

---

# 24. Task Lookup

### Request

```http
GET /lookup?lookup_type=task&task_id=TASK001
```

Optional manager filter:

```http
GET /lookup?lookup_type=task&task_id=TASK001&selected_manager=Manager%20One
```

### Parameters

| Parameter          | Type   | Required          | Description             |
| ------------------ | ------ | ----------------- | ----------------------- |
| `lookup_type`      | String | Yes               | Must be `task`          |
| `task_id`          | String | No at route level | Task ID to search       |
| `selected_manager` | String | No                | Optional manager filter |

### Service

```python
get_employees_with_visible_task(
    task_id,
    selected_manager
)
```

### Response

Returns employees currently visible on the specified task.

Example:

```json
[
    {
        "employee_id": "emp001",
        "employee_name": "john doe",
        "manager": "Manager One",
        "last_log_time": "2026-07-24 00:30:45"
    }
]
```

### Lookup Logic

The service:

1. Finds the latest submission for each employee.
2. Optionally filters by manager.
3. Matches the requested task ID.
4. Returns matching employees.

Task ID comparison is case-insensitive:

```sql
LOWER(t.task_id) = LOWER(?)
```

---

# 25. Invalid Lookup Type

If:

```text
lookup_type
```

is neither:

```text
employee
```

nor:

```text
task
```

the endpoint returns:

```json
{
    "error": "Invalid lookup type"
}
```

### Important Note

The current implementation returns this response with HTTP status:

```text
200 OK
```

A future implementation should preferably return:

```text
400 Bad Request
```

because the client supplied an invalid lookup type.

---

# 26. Task Status Report API

## `GET /task-status-report`

### Purpose

Returns the number of employees associated with each task for a selected date, manager, and task status.

### Query Parameters

| Parameter          | Type   | Default | Description            |
| ------------------ | ------ | ------- | ---------------------- |
| `selected_manager` | String | `All`   | Manager filter         |
| `selected_date`    | String | `None`  | Date filter            |
| `task_status`      | String | `None`  | Task status/job filter |

### Example

```http
GET /task-status-report
```

### Example with filters

```http
GET /task-status-report?selected_date=2026-07-24&selected_manager=Manager%20One&task_status=Flow
```

---

# 27. Task Status Report Response

Example:

```json
[
    {
        "task_id": "task001",
        "employee_count": 5
    },
    {
        "task_id": "task002",
        "employee_count": 3
    }
]
```

### Response Type

```text
application/json
```

### Database Logic

The service:

1. Defaults the date to today if no date is provided.
2. Filters submissions by date.
3. Optionally filters by manager.
4. Optionally filters by `tasks.jobs`.
5. Groups results by task ID.
6. Counts distinct employees.
7. Orders by employee count descending.

Conceptually:

```text
Date
 │
 ▼
Manager Filter
 │
 ▼
Task Status Filter
 │
 ▼
Group by Task
 │
 ▼
Count Employees
 │
 ▼
Sort Descending
```

---

# 28. Task Status Filter Behavior

The task status API uses:

```python
if task_status:
```

Therefore, the following values are treated differently:

```text
None
""
"Flow"
"Dry"
```

An empty string does not add a task status filter.

However, the default value of the API parameter is:

```python
task_status: str = "None"
```

This means that if the endpoint is called without a `task_status` query parameter, the literal string:

```text
"None"
```

may be passed to the service and used as:

```sql
t.jobs = 'None'
```

This is an important implementation detail.

The intended behavior may instead be to use:

```python
task_status: str | None = None
```

or interpret `"None"` as no filter.

---

# 29. Manager Filter Behavior

Several services use:

```python
manager and manager != "All"
```

Therefore:

```text
manager = "All"
```

means:

```text
Do not filter by manager
```

A specific manager name means:

```text
Filter results to that manager
```

This convention is used by:

* `get_latest_submissions()`
* `get_employee_status_counts()`
* `get_task_visibility()`
* `get_idle_employees()`
* `get_employee_visible_tasks()`
* `get_employees_with_visible_task()`
* `get_task_status_report()`

The `"All"` convention should be standardized across all manager APIs.

---

# 30. API and Database Relationship

The API interacts with the following database entities:

```text
managers
    │
    └── Manager names


submissions
    │
    ├── employee_id
    ├── employee_name
    ├── manager
    ├── current_task
    ├── idle
    ├── drive_link
    ├── idle_remarks
    └── submitted_at
         │
         │ 1-to-many
         ▼
tasks
    │
    ├── submission_id
    ├── task_id
    ├── task_name
    ├── sway
    ├── mm
    ├── jobs
    └── remarks
```

Relationship:

```text
submissions.id
      │
      │
      ▼
tasks.submission_id
```

One submission can contain multiple tasks.

---

# 31. Complete API Data Flow

## Employee Submission

```text
employee.html
      │
      ▼
script.js
      │
      │ POST /submit
      ▼
routes/employee.py
      │
      ▼
request.json()
      │
      ▼
save_submission(data)
      │
      ├── Insert submissions row
      │
      ├── Get submission ID
      │
      ├── Insert task 1
      ├── Insert task 2
      ├── Insert task N
      │
      ▼
connection.commit()
      │
      ▼
JSON Response
```

---

## Manager Dashboard

```text
manager.html
      ▲
      │
      │ Template Response
      │
routes/manager.py
      │
      ├── get_all_submissions()
      ├── get_latest_submissions()
      ├── get_managers()
      ├── get_employee_status_counts()
      ├── get_task_visibility()
      ├── get_idle_employees()
      └── get_task_status_report()
              │
              ▼
         SQLite Database
```

---

## Manager Lookup

```text
manager.js
      │
      │ GET /lookup
      ▼
manager_lookup()
      │
      ├── lookup_type=employee
      │       │
      │       ▼
      │ get_employee_visible_tasks()
      │
      └── lookup_type=task
              │
              ▼
        get_employees_with_visible_task()
              │
              ▼
         JSON Response
```

---

# 32. Current API Endpoint Summary

| Method | Endpoint              | Purpose                      | Response |
| ------ | --------------------- | ---------------------------- | -------- |
| `GET`  | `/`                   | Employee router health check | JSON     |
| `POST` | `/submit`             | Save employee submission     | JSON     |
| `GET`  | `/page`               | Render employee page         | HTML     |
| `GET`  | `/managers`           | Get manager list             | JSON     |
| `GET`  | `/`                   | Render manager dashboard     | HTML     |
| `GET`  | `/lookup`             | Employee/task lookup         | JSON     |
| `GET`  | `/task-status-report` | Task status report           | JSON     |

The full paths depend on the router prefixes configured in `app/main.py`.

---

# 33. Current API Architecture

The current API architecture is:

```text
                         Browser
                            │
            ┌───────────────┴───────────────┐
            │                               │
            ▼                               ▼
      Employee UI                      Manager UI
            │                               │
            ▼                               ▼
     employee.py                       manager.py
            │                               │
            │                               ├── get_all_submissions()
            │                               ├── get_latest_submissions()
            │                               ├── get_managers()
            │                               ├── get_employee_status_counts()
            │                               ├── get_task_visibility()
            │                               ├── get_idle_employees()
            │                               ├── get_employee_visible_tasks()
            │                               ├── get_employees_with_visible_task()
            │                               └── get_task_status_report()
            │
            ▼
    save_submission()
            │
            └───────────────┬────────────────┘
                            │
                            ▼
                       database.py
                            │
                            ▼
                       tracker.db
```

---

# 34. Recommended API Improvements

The current API works, but the following improvements are recommended as the project evolves.

## 34.1 Use the Pydantic Submission Model

The project already imports:

```python
from app.models.employee import EmployeeSubmission
```

but the endpoint currently accepts:

```python
request: Request
```

and manually calls:

```python
data = await request.json()
```

Recommended:

```python
@router.post("/submit")
async def submit_employee(data: EmployeeSubmission):
    save_submission(data.model_dump())
    return {"message": "Data received successfully"}
```

Benefits:

* Automatic validation.
* Clear API contract.
* Better Swagger documentation.
* Better error responses.
* Fewer runtime `KeyError` exceptions.

---

## 34.2 Validate Manager Before Submission

The current submission service directly saves the manager received from the frontend.

Recommended future flow:

```text
POST /submit
     │
     ▼
Validate Request
     │
     ▼
Validate Manager
     │
     ├── Invalid → 400 / 422
     │
     ▼
Save Submission
```

This prevents invalid manager values from entering the database.

---

## 34.3 Move Database Queries Behind a Repository

Current:

```text
Route
   │
   ▼
Service
   │
   ▼
get_connection()
   │
   ▼
SQL
```

Future:

```text
Route
   │
   ▼
Service
   │
   ▼
Repository
   │
   ▼
Database
```

This will make future migration from SQLite to PostgreSQL easier.

---

## 34.4 Add API Prefixes

The current routes would be easier to understand if separated into explicit namespaces.

Recommended:

```text
/api/employee/submit
/api/employee/managers

/api/manager/lookup
/api/manager/task-status-report
```

HTML pages can remain separate:

```text
/employee/page
/manager/
```

---

## 34.5 Add Explicit Error Status Codes

Current invalid lookup:

```json
{
    "error": "Invalid lookup type"
}
```

returns HTTP `200`.

Recommended:

```text
400 Bad Request
```

with:

```json
{
    "error": "Invalid lookup type"
}
```

---

## 34.6 Add Dedicated API Response Models

Future APIs should use Pydantic response models.

For example:

```text
EmployeeSubmissionResponse
ManagerLookupResponse
TaskStatusReportResponse
```

This improves:

* Documentation.
* Type safety.
* Frontend integration.
* API consistency.

---

## 34.7 Standardize Date Parameters

The API currently expects dates as strings.

Recommended format:

```text
YYYY-MM-DD
```

Example:

```text
2026-07-24
```

Future Pydantic models can validate this automatically.

---

# 35. Recommended Future API Structure

The current application can gradually evolve toward:

```text
/api
│
├── /employee
│   ├── POST /submit
│   └── GET /managers
│
├── /manager
│   ├── GET /submissions
│   ├── GET /lookup
│   ├── GET /task-status-report
│   ├── GET /idle-employees
│   └── GET /task-visibility
│
├── /dashboard
│   └── GET /summary
│
└── /exports
    └── GET /submissions.csv
```

This is a future target and does not need to be implemented immediately.

---

# 36. API Development Rules

Future API development should follow these rules:

1. Use Pydantic request models for structured input.
2. Use Pydantic response models for important API responses.
3. Keep routes thin.
4. Keep business logic in services.
5. Keep SQL/database operations out of routes.
6. Validate manager values on the backend.
7. Validate enum-like values such as `jobs`.
8. Use consistent HTTP status codes.
9. Return `4xx` for client errors.
10. Return `5xx` for unexpected server errors.
11. Use `GET` for retrieval.
12. Use `POST` for creating submissions.
13. Document every new endpoint.
14. Add automated tests for critical endpoints.
15. Keep API contracts backward-compatible where possible.

---

# 37. Current API Architecture Summary

The current API is intentionally simple:

```text
FastAPI
   │
   ├── Employee Routes
   │      ├── Health Check
   │      ├── Employee Page
   │      ├── Manager List
   │      └── Submission
   │
   └── Manager Routes
          ├── Dashboard
          ├── Lookup
          └── Task Status Report
```

The API currently uses the service layer for database operations:

```text
Routes
   │
   ▼
Services
   │
   ▼
SQLite
```

The recommended long-term architecture is:

```text
Routes
   │
   ▼
Pydantic Schemas
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

The main architectural goal is to preserve a clean separation between **HTTP handling**, **request validation**, **business logic**, and **data persistence** as the MM Task Tracker grows.
