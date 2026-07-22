from datetime import datetime
from app.db.database import get_connection


def get_all_submissions():
    """
    Retrieve all submissions from the database.

    Returns:
        list[dict]: A list of submissions, each represented as a dictionary.
    """
    connection = get_connection()
    cursor = connection.cursor()

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

    return [dict(row) for row in rows]


def get_managers():
    """
    Retrieve all manager names from the database.

    Returns:
        list[str]: A list of manager names.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM managers
        ORDER BY name
    """)

    rows = cursor.fetchall()
    connection.close()

    return [row["name"] for row in rows]


def get_latest_submissions(selected_date: str | None = None, manager: str | None = None):
    connection = get_connection()
    cursor = connection.cursor()

    conditions, params = [], []

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
    connection = get_connection()
    cursor = connection.cursor()

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

    if manager and manager != "All":
        rows = [row for row in rows if row["manager"] == manager]

    total = len(rows)
    idle = sum(1 for row in rows if row["idle"] == 1)
    production = total - idle

    connection.close()

    return {"total": total, "idle": idle, "production": production}


def get_task_visibility(selected_date: str | None = None, manager: str | None = None):
    connection = get_connection()
    cursor = connection.cursor()

    conditions, params = [], []

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


def get_employees_with_visible_task(task_id: str, manager: str | None = None):
    connection = get_connection()
    cursor = connection.cursor()

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
    """

    params = []
    if manager and manager != "All":
        query += " WHERE manager = ?"
        params.append(manager)

    query += """
            GROUP BY employee_id
        ) latest ON s.id = latest.latest_submission_id
        WHERE LOWER(t.task_id) = LOWER(?)
        ORDER BY s.employee_name
    """

    params.append(task_id)
    cursor.execute(query, params)

    rows = cursor.fetchall()
    connection.close()

    return rows


def get_employee_visible_tasks(employee_id: str, manager: str | None = None):
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
    connection = get_connection()
    cursor = connection.cursor()

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
