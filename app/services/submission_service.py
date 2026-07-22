# Import database connection helper
from app.db.database import get_connection
# Import datetime for timestamping submissions
from datetime import datetime

def save_submission(data):
    """
    Save a submission record into the 'submissions' table,
    along with its related tasks into the 'tasks' table.
    """

    # Establish a database connection
    connection = get_connection()
    cursor = connection.cursor()

    # Generate current timestamp in "YYYY-MM-DD HH:MM:SS" format
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert submission details into the 'submissions' table
    cursor.execute(
        """
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["employeeId"].strip().lower(),          # employee_id
            data["employeeName"].strip().lower(),        # employee_name
            data["manager"],             # manager
            data["currentTask"],         # current_task
            1 if data["idle"] else 0,    # idle (boolean → integer)
            data["driveLink"],           # drive_link
            data["idleRemarks"],         # idle_remarks
            submitted_at                 # submitted_at
        )
    )

    # Get the auto-generated submission ID
    submission_id = cursor.lastrowid

    # Insert each task related to this submission into the 'tasks' table
    for task in data["tasks"]:
        cursor.execute(
            """
            INSERT INTO tasks (
                submission_id,
                task_id,
                task_name,
                sway,
                mm,
                jobs,
                remarks
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                submission_id,                # Foreign key linking to submissions
                task["id"].strip().lower(),                   # task_id
                task["name"],                 # task_name
                1 if task["sway"] else 0,     # sway (boolean → integer)
                1 if task["mm"] else 0,       # mm (boolean → integer)
                task["jobs"],                 # jobs
                task["remarks"]               # remarks
            )
        )

    # Print the submission ID for debugging/logging
    print(f"Submission saved with ID: {submission_id}")

    # Commit changes and close the connection
    connection.commit()
    connection.close()
