"""
CRUD Operations Base Class.

Provides generic Create, Read, Update, and Delete operations
for SQLAlchemy ORM models.
"""

from typing import Any, Dict, Type
from sqlalchemy.orm import Session

class CRUDBase:
    """
    Generic class providing basic CRUD (Create, Read, Update, Delete) operations for a given SQLAlchemy model.
    Attributes:
        model (Type[Any]): The SQLAlchemy model class to perform operations on.
    """
    def __init__(self, model: Type[Any]):
        """
        Initialize the CRUDBase with a specific SQLAlchemy model.
        Args:
            model (Type[Any]): The SQLAlchemy model class.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Any:
        """
        Retrieve a single record by its primary key.
        Args:
            db (Session): SQLAlchemy database session.
            id (Any): Primary key of the record.
        Returns:
            Any: The retrieved database record, or None if not found.
        """
        return db.query(self.model).get(id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Any]:
        """
        Retrieve multiple records with optional pagination.
        Args:
            db (Session): SQLAlchemy database session.
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to retrieve. Defaults to 100.
        Returns:
            list[Any]: List of retrieved database records.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> Any:
        """
        Create a new database record.
        Args:
            db (Session): SQLAlchemy database session.
            obj_in (Dict[str, Any]): Dictionary containing fields and values for the new record.
        Returns:
            Any: The newly created database record.
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Any, update_data: Dict[str, Any]) -> Any:
        """
        Update an existing database record.
        Args:
            db (Session): SQLAlchemy database session.
            db_obj (Any): The database record to update.
            update_data (Dict[str, Any]): Dictionary containing fields and updated values.
        Returns:
            Any: The updated database record.
        """
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any) -> Any:
        """
        Delete a database record by its primary key.
        Args:
            db (Session): SQLAlchemy database session.
            id (Any): Primary key of the record to delete.
        Returns:
            Any: The deleted database record, or None if not found.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

