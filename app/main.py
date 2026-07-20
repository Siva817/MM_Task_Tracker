# Import FastAPI core class for creating the application
from fastapi import FastAPI
# Import employee router for modular route handling
from app.routes.employee import router as employee_router
# Import Jinja2Templates for rendering HTML templates
from fastapi.templating import Jinja2Templates
# Import StaticFiles for serving static assets (CSS, JS, images)
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI application instance
app = FastAPI(
    title="MM Task Tracker",
    description="A FastAPI application to track employee tasks and events.",
    version="1.0.0"
)

# Configure Jinja2 templates directory
templates = Jinja2Templates(directory="app/templates")

# Mount static files directory so assets can be served at /static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include employee router with a prefix and tag for grouping endpoints
app.include_router(
    employee_router,
    prefix="/employee",   # All employee routes will start with /employee
    tags=["Employee"]     # Tag used for API documentation grouping
)

@app.get("/")
def home():
    """
    Root endpoint of the application.
    Returns a simple JSON welcome message.
    """
    return {"message": "Welcome to MM Task Tracker!"}
