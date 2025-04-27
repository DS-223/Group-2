from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# ========== DIMENSION SCHEMAS ==========

class DimTableBase(BaseModel):
    nfc_wifi_tag: Optional[str]
    nfc_menu_tag: Optional[str]
    nfc_review_tag: Optional[str]

class DimTableCreate(DimTableBase):
    pass

class DimTableOut(DimTableBase):
    table_id: int
    class Config:
        orm_mode = True


class DimTimeBase(BaseModel):
    date: Optional[date]
    day_of_week: Optional[str]
    month: Optional[int]
    year: Optional[int]
    is_weekend: Optional[bool]

class DimTimeCreate(DimTimeBase):
    pass

class DimTimeOut(DimTimeBase):
    time_id: int
    class Config:
        orm_mode = True


class DimMenuItemBase(BaseModel):
    item_name: Optional[str]
    price: Optional[float]
    category: Optional[str]

class DimMenuItemCreate(DimMenuItemBase):
    pass

class DimMenuItemOut(DimMenuItemBase):
    item_id: int
    class Config:
        orm_mode = True


# ========== FACT SCHEMAS ==========

class FactTransactionItemBase(BaseModel):
    quantity: int
    price: float

class FactTransactionItemCreate(FactTransactionItemBase):
    item_id: int

class FactTransactionItemOut(FactTransactionItemBase):
    transaction_id: int
    item_id: int
    class Config:
        orm_mode = True


class FactTransactionBase(BaseModel):
    total_amount: Optional[float]

class FactTransactionCreate(FactTransactionBase):
    table_id: int
    time_id: int
    created_at: datetime
    items: List[FactTransactionItemCreate]

class FactTransactionOut(FactTransactionBase):
    transaction_id: int
    table_id: int
    mobile_id: str
    time_id: int
    created_at: datetime
    items: List[FactTransactionItemOut]
    class Config:
        orm_mode = True


# ========== ENGAGEMENT + CAMPAIGN SCHEMAS ==========

class NfcEngagementBase(BaseModel):
    tag_type: str
    mobile_id: str
    engagement_time: datetime

class NfcEngagementCreate(NfcEngagementBase):
    table_id: int

class NfcEngagementOut(NfcEngagementBase):
    engagement_id: int
    table_id: int
    class Config:
        orm_mode = True


class MarketingCampaignBase(BaseModel):
    name: str
    target_segment: str
    description: Optional[str]

class MarketingCampaignCreate(MarketingCampaignBase):
    start_time_id: int
    end_time_id: int

class MarketingCampaignOut(MarketingCampaignBase):
    campaign_id: int
    start_time_id: int
    end_time_id: int
    class Config:
        orm_mode = True

class DimUserOut(BaseModel):
    mobile_id: str
    # add more fields as needed

    class Config:
        orm_mode = True


class RFMResultCreate(BaseModel):
    mobile_id: str
    recency_days: int
    frequency: int
    monetary: float
    R_score: int
    F_score: int
    M_score: int
    RFM_score: str
    segment: str
    date_created: datetime

class RFMResultOut(RFMResultCreate):
    rfm_id: int

    class Config:
        orm_mode = True
