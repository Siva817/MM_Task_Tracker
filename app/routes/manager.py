from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.manager import (
    get_all_submissions,
    get_latest_submissions,
    get_managers,
    get_employee_status_counts,
    get_task_visibility,
    get_employee_visible_tasks,
    get_employees_with_visible_task,
    get_idle_employees,
)

# Create router instance
router = APIRouter()

# Jinja2 template directory
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def manager_page(
    request: Request,
    selected_date: str | None = None,
    selected_manager: str | None = None,
):
    """
    Manager dashboard page.
    Displays submissions, status counts, task visibility, and idle employees.
    """

    # Fetch all submissions
    submissions = get_all_submissions()

    # Fetch latest submissions filtered by date/manager
    latest_submissions = get_latest_submissions(
        selected_date,
        selected_manager,
    )

    # Fetch list of managers
    managers = get_managers()

    # Get employee status counts (idle vs production)
    status_counts = get_employee_status_counts(
        selected_date,
        selected_manager,
    )

    # Get task visibility data
    task_visibility = get_task_visibility(
        selected_date,
        selected_manager,
    )

    # Get idle employees list
    idle_employees = get_idle_employees(
        selected_date,
        selected_manager,
    )

    # Debug print for idle employees
    print("\n===== Idle Employees =====")
    for employee in idle_employees:
        print(dict(employee))
    print("===== End Idle Employees =====\n")

    # Render template with context data
    return templates.TemplateResponse(
        request,
        "manager.html",
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
        },
    )


@router.get("/lookup")
async def manager_lookup(
    lookup_type: str,
    employee_id: str | None = None,
    task_id: str | None = None,
    selected_manager: str | None = None,
):
    """
    Lookup endpoint.
    Allows searching either by employee (visible tasks) or task (employees with task visible).
    """

    # Lookup by employee ID
    if lookup_type == "employee":
        rows = get_employee_visible_tasks(
            employee_id,
            selected_manager,
        )
        return [
            {
                "employee_id": row["employee_id"],
                "employee_name": row["employee_name"],
                "manager": row["manager"],
                "submitted_at": row["submitted_at"],
                "task_id": row["task_id"],
                "task_name": row["task_name"],
                "jobs": row["jobs"],
                "remarks": row["remarks"],
            }
            for row in rows
        ]

    # Lookup by task ID
    if lookup_type == "task":
        rows = get_employees_with_visible_task(
            task_id,
            selected_manager,
        )
        return [
            {
                "employee_id": row["employee_id"],
                "employee_name": row["employee_name"],
                "manager": row["manager"],
                "last_log_time": row["last_log_time"],
            }
            for row in rows
        ]

    # Invalid lookup type
    return {"error": "Invalid lookup type"}
