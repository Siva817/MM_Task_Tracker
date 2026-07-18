from enum import Enum

class EventType(str, Enum):
    LOGIN = "Login"
    TASK_SWITCH = "Task Switch"
    TASK_DISAPPEARED = "Task Disappeared"
    NO_JOBS = "No Jobs"
    ASSESSMENT_CLEARED = "Assessment Cleared"