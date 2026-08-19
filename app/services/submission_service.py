from datetime import datetime

from sqlalchemy import text

from app.db.database import engine


def save_submission(data):
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with engine.begin() as connection:

        result = connection.execute(
            text("""
                INSERT INTO submissions (
                    employee_id,
                    employee_name,
                    manager,
                    current_task,
                    idle,
                    drive_link,
                    idle_remarks,
                    submitted_at
                )
                OUTPUT INSERTED.id
                VALUES (
                    :employee_id,
                    :employee_name,
                    :manager,
                    :current_task,
                    :idle,
                    :drive_link,
                    :idle_remarks,
                    :submitted_at
                )
            """),
            {
                "employee_id": data["employeeId"].strip().lower(),
                "employee_name": data["employeeName"].strip().lower(),
                "manager": data["manager"],
                "current_task": data["currentTask"],
                "idle": 1 if data["idle"] else 0,
                "drive_link": data["driveLink"],
                "idle_remarks": data["idleRemarks"],
                "submitted_at": submitted_at,
            },
        )

        submission_id = result.scalar_one()

        for task in data["tasks"]:
            connection.execute(
                text("""
                    INSERT INTO tasks (
                        submission_id,
                        task_id,
                        task_name,
                        sway,
                        mm,
                        jobs,
                        remarks
                    )
                    VALUES (
                        :submission_id,
                        :task_id,
                        :task_name,
                        :sway,
                        :mm,
                        :jobs,
                        :remarks
                    )
                """),
                {
                    "submission_id": submission_id,
                    "task_id": task["id"].strip().lower(),
                    "task_name": task["name"],
                    "sway": 1 if task["sway"] else 0,
                    "mm": 1 if task["mm"] else 0,
                    "jobs": task["jobs"],
                    "remarks": task["remarks"],
                },
            )

    print(f"Submission saved with ID: {submission_id}")