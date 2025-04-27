"""
Database Configuration.

Sets up the SQLAlchemy engine, base class, and session factory for database operations.
"""

import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

def get_db():
    """
    Provide a database session.
    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

load_dotenv('.env')


DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine = sql.create_engine(DATABASE_URL, echo=True)


Base = declarative_base()

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


