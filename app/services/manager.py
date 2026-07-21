from app.db.database import get_connection


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

    # Convert rows to dictionaries for easier handling
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

    # Extract only the 'name' field from each row
    return [row["name"] for row in rows]


def get_latest_submissions(selected_date=None, manager=None):
    connection = get_connection()
    cursor = connection.cursor()

    conditions = []
    params = []

    if selected_date:
        conditions.append("DATE(submitted_at) = ?")
        params.append(selected_date)

    if manager and manager != "All":
        conditions.append("manager = ?")
        params.append(manager)

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

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

def get_employee_status_counts(selected_date=None, manager=None):
    connection = get_connection()
    cursor = connection.cursor()

    if selected_date:
        date_filter = "WHERE DATE(submitted_at) = ?"
        params = [selected_date]
    else:
        date_filter = ""
        params = []

    # Get latest submission for each employee
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

    # Apply manager filter
    if manager and manager != "All":
        rows = [
            row for row in rows
            if row["manager"] == manager
        ]

    total = len(rows)

    idle = sum(
        1 for row in rows
        if row["idle"] == 1
    )

    production = total - idle

    connection.close()

    return {
        "total": total,
        "idle": idle,
        "production": production
    }

def get_task_visibility(selected_date=None, manager=None):
    connection = get_connection()
    cursor = connection.cursor()

    conditions = []
    params = []

    if selected_date:
        conditions.append("DATE(s.submitted_at) = ?")
        params.append(selected_date)

    if manager and manager != "All":
        conditions.append("s.manager = ?")
        params.append(manager)

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    cursor.execute(f"""
        SELECT
            t.task_id,
            t.task_name,
            COUNT(DISTINCT s.employee_id) AS employee_count
        FROM tasks t
        INNER JOIN submissions s
            ON t.submission_id = s.id

        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions s
            {where_clause}
            GROUP BY employee_id
        ) latest
            ON s.id = latest.latest_submission_id

        GROUP BY t.task_id, t.task_name
        ORDER BY employee_count DESC
    """, params)

    rows = cursor.fetchall()

    connection.close()

    return rows