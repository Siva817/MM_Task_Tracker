# Import the function that provides a database connection
from app.db.database import get_connection

def initialize_database():
    """
    Initialize the database by creating the 'submissions' table
    if it does not already exist.
    """

    # Get a connection object from the database module
    connection = get_connection()   # ✅ must call the function

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()    # ✅ must call the method

    # Execute SQL command to create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            employee_name TEXT,
            manager TEXT,
            current_task TEXT,
            idle INTEGER,
            drive_link TEXT,
            idle_remarks TEXT,
            submitted_at TEXT
        )
    """)

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            task_id TEXT,
            task_name TEXT,
            sway INTEGER,
            mm INTEGER,
            jobs TEXT,
            remarks TEXT,
            FOREIGN KEY (submission_id) REFERENCES submissions(id)
        )
    """)

    # Commit changes to the database
    connection.commit()

    # Close the connection
    connection.close()


# Run the function only if this script is executed directly
if __name__ == "__main__":
    initialize_database()
