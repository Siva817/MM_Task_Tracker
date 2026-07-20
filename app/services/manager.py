from app.db.database import get_connection


def get_all_submissions():

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