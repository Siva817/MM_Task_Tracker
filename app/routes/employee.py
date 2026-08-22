# FastAPI imports for routing, request handling, and responses
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.manager import get_managers

# Create a router instance for employee-related endpoints
router = APIRouter()

# Configure Jinja2 templates directory for rendering HTML pages
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def employee_home():
    """
    Basic health check route for employee endpoints.
    Returns a simple JSON message confirming the router is working.
    """
    return {"message": "Employee Routes Working!"}


@router.post("/submit")
async def submit_employee(request: Request):
    """
    Endpoint to handle employee submissions.
    - Accepts JSON payload from the request body.
    - Saves submission data into the database.
    - Logs the submission for debugging.
    - Returns a success message.
    """

    # Parse JSON data from the request
    data = await request.json()

    # Debugging/logging output
    # print("\n====== Employee Submission ===")
    # save_submission(data)   # Save data using the service layer
    # print(data)
    # print("====== End Employee Submission ===\n")

    # Response back to client
    return {"message": "Data received successfully"}


@router.get("/page", response_class=HTMLResponse)
def employee_page(request: Request):
    """
    Endpoint to render the employee HTML page using Jinja2 templates.
    - Returns an HTML response with the 'employee.html' template.
    - Provides request context for template rendering.
    """
    return templates.TemplateResponse(
        request=request,
        name="employee.html",
        context={}
    )

@router.get("/managers")
async def managers():

    return get_managers()