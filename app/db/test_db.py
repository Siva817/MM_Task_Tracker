from sqlalchemy import create_engine, text

connection_string = (
    "mssql+pyodbc://@LAPTOP-571GK83L/MMTaskTracker"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(connection_string)

with engine.connect() as connection:
    result = connection.execute(text("SELECT @@VERSION"))
    print(result.fetchone()[0])
    