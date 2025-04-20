"""
Database Configuration
"""
import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os

def get_db():
    """
    Function to get a database session. 
    Yields a session, then closes it when done.
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


