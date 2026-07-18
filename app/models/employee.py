from pydantic import BaseModel
from typing import List

from app.models.enum import EventType

class EmployeeSubmission(BaseModel):
    emp_id: str
    employee_name: str
    manager: str
    event_type: EventType
    current_task: str
    visible_tasks: List[str]