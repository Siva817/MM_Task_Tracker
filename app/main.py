from fastapi import FastAPI
from app.routes.employee import router as employee_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(
    employee_router,
    prefix="/employee",
    tags=["Employee"])

@app.get("/")
def home():
    return {
        "message": "Welcome to MM Task Tracker!"
    }