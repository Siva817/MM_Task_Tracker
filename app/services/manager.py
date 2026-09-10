from datetime import datetime

from sqlalchemy import text

from app.db.database import engine


def get_all_submissions():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT employee_id,
                       employee_name,
                       manager,
                       current_task,
                       idle,
                       submitted_at
                FROM submissions
                ORDER BY submitted_at DESC
            """)
        )

        return [dict(row) for row in result.mappings().all()]


def get_managers():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT name
                FROM managers
                ORDER BY name
            """)
        )

        return [row["name"] for row in result.mappings().all()]


def get_latest_submissions(
    selected_date: str | None = None,
    manager: str | None = None
):
    conditions = []
    params = {}

    if selected_date:
        conditions.append("CAST(submitted_at AS DATE) = :selected_date")
        params["selected_date"] = selected_date

    if manager and manager != "All":
        conditions.append("manager = :manager")
        params["manager"] = manager

    where = ""

    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    query = text(f"""
        SELECT *
        FROM submissions
        WHERE id IN (
            SELECT MAX(id)
            FROM submissions
            {where}
            GROUP BY employee_id
        )
        ORDER BY employee_name
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)

        return result.mappings().all()


def get_employee_status_counts(
    selected_date: str | None = None,
    manager: str | None = None
):
    conditions = []
    params = {}

    if selected_date:
        conditions.append("CAST(submitted_at AS DATE) = :selected_date")
        params["selected_date"] = selected_date

    where = ""

    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    query = text(f"""
        SELECT *
        FROM submissions
        WHERE id IN (
            SELECT MAX(id)
            FROM submissions
            {where}
            GROUP BY employee_id
        )
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)
        rows = result.mappings().all()

    if manager and manager != "All":
        rows = [r for r in rows if r["manager"] == manager]

    total = len(rows)
    idle = sum(1 for r in rows if r["idle"] == 1)
    production = total - idle

    return {
        "total": total,
        "idle": idle,
        "production": production,
    }


def get_task_visibility(
    selected_date: str | None = None,
    manager: str | None = None
):
    conditions = []
    params = {}

    if selected_date:
        conditions.append("CAST(submitted_at AS DATE) = :selected_date")
        params["selected_date"] = selected_date

    if manager and manager != "All":
        conditions.append("s.manager = :manager")
        params["manager"] = manager

    where = ""

    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    query = text(f"""
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
            {where}
            GROUP BY employee_id
        ) latest
            ON s.id = latest.latest_submission_id
        GROUP BY t.task_id, t.task_name
        ORDER BY employee_count DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)

        return result.mappings().all()


def get_employees_with_visible_task(
    task_id: str,
    manager: str | None = None,
    selected_date: str | None = None
):
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    params = {
        "selected_date": selected_date,
        "task_id": task_id,
    }

    manager_filter = ""

    if manager and manager != "All":
        manager_filter = "AND manager = :manager"
        params["manager"] = manager

    query = text(f"""
        SELECT
            s.employee_id,
            s.employee_name,
            s.manager,
            s.submitted_at AS last_log_time
        FROM submissions s
        INNER JOIN tasks t
            ON t.submission_id = s.id
        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions
            WHERE CAST(submitted_at AS DATE) = :selected_date
            {manager_filter}
            GROUP BY employee_id
        ) latest
            ON s.id = latest.latest_submission_id
        WHERE LOWER(t.task_id) = LOWER(:task_id)
        ORDER BY s.employee_name
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)

        return result.mappings().all()


def get_tasks_visible_to_employee(
    employee_id: str,
    manager: str | None = None
):
    params = {
        "employee_id": employee_id,
    }

    manager_filter = ""

    if manager and manager != "All":
        manager_filter = "AND manager = :manager"
        params["manager"] = manager

    query = text(f"""
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
        INNER JOIN tasks t
            ON t.submission_id = s.id
        INNER JOIN (
            SELECT
                employee_id,
                MAX(id) AS latest_submission_id
            FROM submissions
            WHERE LOWER(employee_id) = LOWER(:employee_id)
            {manager_filter}
            GROUP BY employee_id
        ) latest
            ON s.id = latest.latest_submission_id
        ORDER BY t.task_name
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)

        return result.mappings().all()


def get_idle_employees(
    selected_date: str | None = None,
    manager: str | None = None
):
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    params = {
        "selected_date": selected_date,
    }

    manager_filter = ""

    if manager and manager != "All":
        manager_filter = "AND manager = :manager"
        params["manager"] = manager

    query = text(f"""
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
            WHERE CAST(submitted_at AS DATE) = :selected_date
            {manager_filter}
            GROUP BY employee_id
        ) latest
            ON s.id = latest.latest_submission_id
        WHERE s.idle = 1
        ORDER BY s.submitted_at DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)

        return result.mappings().all()


def get_task_status_report(
    selected_date=None,
    manager=None,
    task_status=None
):
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    params = {
        "selected_date": selected_date,
    }

    conditions = [
        "CAST(submitted_at AS DATE) = :selected_date"
    ]

    if manager and manager != "All":
        conditions.append("s.manager = :manager")
        params["manager"] = manager

    if task_status:
        conditions.append("t.jobs = :task_status")
        params["task_status"] = task_status

    query = text(f"""
        SELECT
            t.task_id,
            COUNT(DISTINCT s.employee_id) AS employee_count
        FROM tasks t
        INNER JOIN submissions s
            ON t.submission_id = s.id
        WHERE {" AND ".join(conditions)}
        GROUP BY t.task_id
        ORDER BY employee_count DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query, params)

        return result.mappings().all()

def get_op_manager_summary(selected_date: str | None = None):
    if not selected_date:
        selected_date = datetime.now().strftime("%Y-%m-%d")

    params = {"selected_date": selected_date}

    query = text("""
        SELECT
            manager,
            COUNT(*) AS total,
            SUM(CASE WHEN idle = 1 THEN 1 ELSE 0 END) AS idle
        FROM submissions
        WHERE id IN (
            SELECT MAX(id)
            FROM submissions
            WHERE CAST(submitted_at AS DATE) = :selected_date
            GROUP BY employee_id
        )
        GROUP BY manager
        ORDER BY manager
    """)

    with engine.connect() as connection:
        rows = connection.execute(query, params).mappings().all()

    return [
        {
            "manager": row["manager"],
            "idle": row["idle"] or 0,
            "production": (row["total"] or 0) - (row["idle"] or 0),
            "total": row["total"] or 0,
        }
        for row in rows
    ]