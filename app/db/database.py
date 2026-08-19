import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")

connection_url = URL.create(
    "mssql+pyodbc",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "server": SQL_SERVER,
        "database": SQL_DATABASE,
        "trusted_connection": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
)