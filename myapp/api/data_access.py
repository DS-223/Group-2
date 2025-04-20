from typing import Any, Dict, Type
from sqlalchemy.orm import Session

class CRUDBase:
    """
    Generic CRUD operations.
    Methods:
      - get: retrieve by primary key
      - get_all: list with pagination
      - create: insert new record
      - update: modify existing record
      - delete: delete record
    """
    def __init__(self, model: Type[Any]):
        self.model = model

    def get(self, db: Session, id: Any) -> Any:
        return db.query(self.model).get(id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Any]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> Any:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Any, update_data: Dict[str, Any]) -> Any:
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any) -> Any:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

