# Import BaseModel from Pydantic for data validation and serialization
from pydantic import BaseModel
# Import List type hint for defining lists of strings
from typing import List

# Import custom Enum for event types
from app.models.enum import EventType

class EmployeeSubmission(BaseModel):
    """
    Pydantic model representing an employee's task submission.
    Ensures type validation and structured data handling.
    """

    emp_id: str                  # Unique identifier for the employee
    employee_name: str           # Full name of the employee
    manager: str                 # Manager responsible for the employee
    event_type: EventType        # Type of event (defined in EventType enum)
    current_task: str            # Description of the employee's current task
    visible_tasks: List[str]     # List of tasks visible/assigned to the employee