from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.manager import (get_all_submissions, get_managers)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def manager_page(request: Request):

    submissions = get_all_submissions()
    managers = get_managers()

    print("\n===== Manager Dashboard Data =====")
    print(dict(submissions[0]))
    print("===== End =====\n")

    return templates.TemplateResponse(
        request,
        "manager.html",
        {
            "request": request,
            "submissions": submissions,
            "managers": managers
        }
    )

