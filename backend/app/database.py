from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME")

ODBC_DRIVER = "ODBC Driver 18 for SQL Server"

connection_string = (
    f"DRIVER={{{ODBC_DRIVER}}};"
    f"SERVER={DB_HOST},{DB_PORT};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

DATABASE_URL = "mssql+pyodbc:///?odbc_connect=" + quote_plus(connection_string)

engine = create_engine( 
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
