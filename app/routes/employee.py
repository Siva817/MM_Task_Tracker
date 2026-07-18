from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.employee import EmployeeSubmission
from fastapi.responses import PlainTextResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def employee_home():
    return {
        "message": "Employee Routes Working!"
    }

@router.post("/submit")
def submit_employee(submission: EmployeeSubmission):
    print(submission)

    return {
        "status": "success",
        "message": "Submission received!"
    }

@router.get("/page", response_class=HTMLResponse)
def employee_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="employee.html",
        context={}
    )
  