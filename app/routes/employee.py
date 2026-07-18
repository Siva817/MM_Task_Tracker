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
async def submit_employee(request: Request):

    data = await request.json()

    print("\n====== Employee Submission ===")
    print(data)
    print("====== End Employee Submission ===\n")

    return {
        "message": "Data received successfully"
    }

@router.get("/page", response_class=HTMLResponse)
def employee_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="employee.html",
        context={}
    )
  