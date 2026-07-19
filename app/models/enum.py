# Import Enum base class for creating enumerations
from enum import Enum

class EventType(str, Enum):
    """
    Enumeration of possible employee event types.
    Each value represents a specific type of activity or state
    that can be recorded in the system.
    """

    LOGIN = "Login"                            # Employee logged into the system
    TASK_SWITCH = "Task Switch"                # Employee switched to a different task
    TASK_DISAPPEARED = "Task Disappeared"      # A task assigned to the employee disappeared
    NO_JOBS = "No Jobs"                        # Employee has no jobs available
    ASSESSMENT_CLEARED = "Assessment Cleared"  # Employee cleared an assessment
