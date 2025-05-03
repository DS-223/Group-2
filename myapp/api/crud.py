# crud_base.py

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
import schemas


# Define generic types
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default Create, Read, Update, Delete (CRUD) operations.

    Parameters:
    - model: A SQLAlchemy model class.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.
        """
        return db.query(self.model).get(id)

    def get_multi(
            self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """
        Update a record.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Delete a record by ID.
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

# 🚀 Fact Transactions
crud_fact_transaction = CRUDBase[
    models.FactTransaction,
    schemas.FactTransactionCreate,
    schemas.FactTransactionUpdate,
](models.FactTransaction)


# 🚀 Fact Transaction Items
crud_fact_transaction_item = CRUDBase[
    models.FactTransactionItem,
    schemas.FactTransactionItemCreate,
    schemas.FactTransactionItemUpdate,
](models.FactTransactionItem)


# 🚀 Dim Menu Daytimes
crud_dim_menu_daytime = CRUDBase[
    models.DimMenuDaytime,
    schemas.DimMenuDaytimeCreate,
    schemas.DimMenuDaytimeUpdate,
](models.DimMenuDaytime)


# 🚀 Menu Recommendations
crud_menu_recommendation = CRUDBase[
    models.MenuRecommendation,
    schemas.MenuRecommendationCreate,
    schemas.MenuRecommendationUpdate,
](models.MenuRecommendation)


# 🚀 Dim Users
crud_dim_user = CRUDBase[
    models.DimUser,
    schemas.DimUserCreate,
    schemas.DimUserUpdate,
](models.DimUser)


# 🚀 RFM Segments
crud_rfm_segment = CRUDBase[
    models.RfmSegment,
    schemas.RfmSegmentCreate,
    schemas.RfmSegmentUpdate,
](models.RfmSegment)


# 🚀 Marketing Campaigns
crud_marketing_campaign = CRUDBase[
    models.MarketingCampaign,
    schemas.MarketingCampaignCreate,
    schemas.MarketingCampaignUpdate,
](models.MarketingCampaign)


# 🚀 Dim Time (for dashboard trends / references)
crud_dim_time = CRUDBase[
    models.DimTime,
    schemas.DimTimeCreate,
    schemas.DimTimeUpdate,
](models.DimTime)


# 🚀 Dim Tables
crud_dim_table = CRUDBase[
    models.DimTable,
    schemas.DimTableCreate,
    schemas.DimTableUpdate,
](models.DimTable)


# 🚀 NFC Engagements
crud_nfc_engagement = CRUDBase[
    models.NfcEngagement,
    schemas.NfcEngagementCreate,
    schemas.NfcEngagementUpdate,
](models.NfcEngagement)


# 🚀 Dim Menu Items
crud_dim_menu_item = CRUDBase[
    models.DimMenuItem,
    schemas.DimMenuItemCreate,
    schemas.DimMenuItemUpdate,
](models.DimMenuItem)