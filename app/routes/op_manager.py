from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.manager import get_op_manager_summary


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def op_manager_page(
    request: Request,
    selected_date: str | None = None
):
    managers = get_op_manager_summary(selected_date)

    return templates.TemplateResponse(
        request,
        "op_manager.html",
        {
            "request": request,
            "selected_date": selected_date,
            "managers": managers,
        },
    )