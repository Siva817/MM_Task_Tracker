import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

connection_url = URL.create(
    "mssql+pyodbc",
    username=SQL_USERNAME,
    password=SQL_PASSWORD,
    host=SQL_SERVER,
    database=SQL_DATABASE,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "no",
    },
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
)