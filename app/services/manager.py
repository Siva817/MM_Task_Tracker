from datetime import datetime
from app.db.database import get_connection

# =====================================
# Database Queries for Submissions & Tasks
# =====================================

def get_all_submissions():
    """
    Retrieve all submissions from the database.

    Returns:
        list[dict]: A list of submissions, each represented as a dictionary.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch all submissions ordered by submission time (latest first)
    cursor.execute("""
        SELECT
            employee_id,
            employee_name,
            manager,
            current_task,
            idle,
            submitted_at
        FROM submissions
        ORDER BY submitted_at DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    # Convert rows to list of dictionaries
    return [dict(row) for row in rows]


def get_managers():
    """
    Retrieve all manager names from the database.

    Returns:
        list[str]: A list of manager names.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch all managers ordered alphabetically
    cursor.execute("""
        SELECT name
        FROM managers
        ORDER BY name
    """)

    rows = cursor.fetchall()
    connection.close()

    return [row["name"] for row in rows]


def get_latest_submissions(selected_date: str | None = None, manager: str | None = None):
    """
    Get the latest submissions per employee, optionally filtered by date and manager.
    """
    connection = get_connection()
    cursor = connection.cursor()

    conditions, params = [], []

    # Apply filters if provided
    if selected_date:
        conditions.append("DATE(submitted_at) = ?")
        params.append(selected_date)

    if manager and manager != "All":
        conditions.append("manager = ?")
        params.append(manager)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    cursor.execute(f"""
        SELECT *
        FROM submissions
        WHERE id IN (
            SELECT MAX(id)
            FROM submissions
            {where_clause}
            GROUP BY employee_id
        )
        ORDER BY employee_name
    """, params)

    rows = cursor.fetchall()
    connection.close()

    return rows


def get_employee_status_counts(selected_date: str | None = None, manager: str | None = None):
    """
    Count employees by status (idle vs production).
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Filter by date if provided
    if selected_date:
        date_filter = "WHERE DATE(submitted_at) = ?"
        params = [selected_date]
    else:
        date_filter, params = "", []

    query = f"""
        SELECT *
        FROM submissions
        WHERE id IN (
            SELECT MAX(id)
            FROM submissions
            {date_filter}
            GROUP BY employee_id
        )
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Apply manager filter if provided
    if manager and manager != "All":
        rows = [row for row in rows if row["manager"] == manager]

    # Calculate counts
    total = len(rows)
    idle = sum(1 for row in rows if row["idle"] == 1)
    production = total - idle

    connection.close()

    return {"total": total, "idle": idle, "production": production}


def get_task_visibility(selected_date: str | None = None, manager: str | None = None):
    """
    Get visibility of tasks (how many employees are working on each task).
    """
    connection = get_connection()
    cursor = connection.cursor()

    conditions, params = [], []

    # Apply filters
    if selected_date:
        conditions.append("DATE(s.submitted_at) = ?")
        params.append(selected_date)

    if manager and manager != "All":
        conditions.append("s.manager = ?")
        params.append(manager)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    cursor.execute(f"""
        SELECT
            t.task_id,
            t.task_name,
            COUNT(DISTINCT s.employee_id) AS employee_count
        FROM tasks t
        INNER JOIN submissions s ON t.submission_id = s.id
        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions s
            {where_clause}
            GROUP BY employee_id
        ) latest ON s.id = latest.latest_submission_id
        GROUP BY t.task_id, t.task_name
        ORDER BY employee_count DESC
    """, params)

    rows = cursor.fetchall()
    connection.close()

    return rows


def get_employees_with_visible_task(
        task_id: str,
        manager: str | None = None,
        selected_date: str | None = None):
    """
    Get employees currently visible on a specific task.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Default to today's date if not provided
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    print("===== TASK LOOKUP DEBUG =====")
    print("Task ID:", task_id)
    print("Manager:", manager)
    print("Selected Date:", selected_date)

    query = """
        SELECT
            s.employee_id,
            s.employee_name,
            s.manager,
            s.submitted_at AS last_log_time
        FROM submissions s
        INNER JOIN tasks t ON t.submission_id = s.id
        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions
            WHERE DATE(submitted_at) = ?
    """

    params = [selected_date]
    if manager and manager != "All":
        query += " AND manager = ?"
        params.append(manager)

    query += """
            GROUP BY employee_id
        ) latest ON s.id = latest.latest_submission_id
        WHERE LOWER(t.task_id) = LOWER(?)
        ORDER BY s.employee_name
    """

    params.append(task_id)

    print("SQL Params:", params)

    cursor.execute(query, params)

    rows = cursor.fetchall()
    
    print("Rows Found:", len(rows))
    print("============================")



    connection.close()

    return rows


def get_tasks_visible_to_employee(employee_id: str, manager: str | None = None):
    """
    Get all tasks visible for a specific employee.
    """
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            s.employee_id,
            s.employee_name,
            s.manager,
            s.submitted_at,
            t.task_id,
            t.task_name,
            t.jobs,
            t.remarks
        FROM submissions s
        INNER JOIN tasks t ON t.submission_id = s.id
        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions
            WHERE LOWER(employee_id) = LOWER(?)
    """

    params = [employee_id]
    if manager and manager != "All":
        query += " AND manager = ?"
        params.append(manager)

    query += """
            GROUP BY employee_id
        ) latest ON s.id = latest.latest_submission_id
        ORDER BY t.task_name
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()

    return rows


def get_idle_employees(selected_date: str | None = None, manager: str | None = None):
    """
    Get employees marked as idle for a given date and manager.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Default to today's date if not provided
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    query = """
        SELECT
            s.employee_id,
            s.employee_name,
            s.manager,
            s.drive_link,
            s.idle_remarks,
            s.submitted_at
        FROM submissions s
        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions
            WHERE DATE(submitted_at) = ?
    """

    params = [selected_date]
    if manager and manager != "All":
        query += " AND manager = ?"
        params.append(manager)

    query += """
            GROUP BY employee_id
        ) latest ON s.id = latest.latest_submission_id
        WHERE s.idle = 1
        ORDER BY s.submitted_at DESC
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()

    return rows


def get_task_status_report(selected_date=None, manager=None, task_status=None):
    """
    Get task status report for a given date, manager, and task status.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Default to today's date if not provided
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    query = """
        SELECT
            t.task_id,
            COUNT(DISTINCT s.employee_id) AS employee_count
        FROM tasks t
        INNER JOIN submissions s ON t.submission_id = s.id
        WHERE DATE(s.submitted_at) = ?
    """

    params = [selected_date]

    # Manager filter
    if manager and manager != "All":
        query += " AND s.manager = ?"
        params.append(manager)

    # Task status filter
    if task_status:
        query += " AND t.jobs = ?"
        params.append(task_status)

    query += """
        GROUP BY t.task_id
        ORDER BY employee_count DESC
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()

    return rows
