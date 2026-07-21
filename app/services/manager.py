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


def get_latest_submissions():
    """
    Retrieve the latest submission for each employee.

    Returns:
        list[dict]: A list of the most recent submissions per employee.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch the most recent submission for each employee
    cursor.execute("""
        SELECT s.*
        FROM submissions s
        INNER JOIN (
            SELECT employee_id, MAX(submitted_at) AS latest_time
            FROM submissions
            GROUP BY employee_id
        ) latest
        ON s.employee_id = latest.employee_id
        AND s.submitted_at = latest.latest_time
        ORDER BY s.employee_name
    """)

    rows = cursor.fetchall()
    connection.close()

    return rows
