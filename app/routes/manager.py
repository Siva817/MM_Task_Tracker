from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.manager import (
    get_all_submissions,
    get_latest_submissions,
    get_managers,
    get_employee_status_counts,
    get_task_visibility)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
async def manager_page(
    request: Request,
    selected_date: str | None = None,
    selected_manager: str | None = None
    ):

    submissions = get_all_submissions()

    latest_submissions = get_latest_submissions(
        selected_date,
        selected_manager
    )

    managers = get_managers()

    status_counts = get_employee_status_counts(
        selected_date,
        selected_manager
    )

    task_visibility = get_task_visibility(
        selected_date,
        selected_manager
    )

    print("\n===== Task Visibility =====")
    print("Selected Manager:", selected_manager)
    print("Selected Date:", selected_date)

    for task in task_visibility:
        print(dict(task))

    print("===== End Task Visibility =====\n")

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
            "selected_manager": selected_manager
        }
    )

