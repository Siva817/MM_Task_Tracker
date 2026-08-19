import os

from dotenv import load_dotenv
from sqlalchemy import text

from app.db.database import engine

load_dotenv()

RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "30"))


def delete_old_data():
    with engine.begin() as connection:

        # Delete tasks first because they belong to submissions
        connection.execute(
            text("""
                DELETE FROM tasks
                WHERE submission_id IN (
                    SELECT id
                    FROM submissions
                    WHERE submitted_at < DATEADD(
                        DAY,
                        -:retention_days,
                        GETDATE()
                    )
                )
            """),
            {"retention_days": RETENTION_DAYS},
        )

        # Delete old submissions
        result = connection.execute(
            text("""
                DELETE FROM submissions
                WHERE submitted_at < DATEADD(
                    DAY,
                    -:retention_days,
                    GETDATE()
                )
            """),
            {"retention_days": RETENTION_DAYS},
        )

        print(
            f"Data cleanup completed. "
            f"Deleted {result.rowcount} old submissions."
        )
