import sqlite3

# Path to the SQLite database file
DATABASE = "app/db/tracker.db"

def get_connection():
    """
    Establish and return a connection to the SQLite database.
    The connection uses sqlite3.Row as the row factory so that
    query results can be accessed like dictionaries (by column name).
    """
    # Create a connection to the database file
    connection = sqlite3.connect(DATABASE)

    # Configure the connection to return rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Return the connection object to the caller
    return connection