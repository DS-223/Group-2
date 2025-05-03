from datetime import date, datetime, time
from typing import Optional, List
from pydantic import BaseModel


# ---------- fact_transactions ----------
class FactTransactionBase(BaseModel):
    mobile_id: str
    table_id: int
    time_id: int
    total_amount: float


class FactTransactionCreate(FactTransactionBase):
    pass


class FactTransactionUpdate(FactTransactionBase):
    pass


class FactTransactionOut(FactTransactionBase):
    transaction_id: int
    created_at: datetime

    class Config:
        from_attributes= True


# ---------- fact_transaction_items ----------
class FactTransactionItemBase(BaseModel):
    transaction_id: int
    item_id: int
    quantity: int
    price: float


class FactTransactionItemCreate(FactTransactionItemBase):
    pass


class FactTransactionItemUpdate(FactTransactionItemBase):
    pass


class FactTransactionItemOut(FactTransactionItemBase):
    class Config:
        from_attributes= True


# ---------- dim_menu_daytimes ----------
class DimMenuDaytimeBase(BaseModel):
    daytime_label: str
    start_time: time
    end_time: time


class DimMenuDaytimeCreate(DimMenuDaytimeBase):
    pass


class DimMenuDaytimeUpdate(DimMenuDaytimeBase):
    pass


class DimMenuDaytimeOut(DimMenuDaytimeBase):
    daytime_id: int

    class Config:
        from_attributes= True


# ---------- menu_recommendations ----------
class MenuRecommendationBase(BaseModel):
    menu_item_id: int
    daytime_id: int
    rank: int


class MenuRecommendationCreate(MenuRecommendationBase):
    pass


class MenuRecommendationUpdate(MenuRecommendationBase):
    pass


class MenuRecommendationOut(MenuRecommendationBase):
    id: int

    class Config:
        from_attributes= True


# ---------- dim_users ----------
class DimUserBase(BaseModel):
    notes: Optional[str] = None


class DimUserCreate(DimUserBase):
    mobile_id: str


class DimUserUpdate(DimUserBase):
    pass


class DimUserOut(DimUserBase):
    mobile_id: str

    class Config:
        from_attributes= True


# ---------- rfm_segments ----------
class RfmSegmentBase(BaseModel):
    mobile_id: str
    recency_days: int
    frequency: int
    monetary: float
    R_score: int
    F_score: int
    M_score: int
    RFM_score: str
    segment: str


class RfmSegmentCreate(RfmSegmentBase):
    pass


class RfmSegmentUpdate(RfmSegmentBase):
    pass


class RfmSegmentOut(RfmSegmentBase):
    rfm_id: int
    date_created: datetime

    class Config:
        from_attributes= True


# ---------- marketing_campaigns ----------
class MarketingCampaignBase(BaseModel):
    name: str
    start_time_id: int
    end_time_id: int
    target_segment: str
    description: Optional[str] = None


class MarketingCampaignCreate(MarketingCampaignBase):
    pass


class MarketingCampaignUpdate(MarketingCampaignBase):
    pass


class MarketingCampaignOut(MarketingCampaignBase):
    campaign_id: int

    class Config:
        from_attributes= True


# ---------- dim_time ----------
class DimTimeBase(BaseModel):
    date: date
    day_of_week: str
    month: int
    year: int
    is_weekend: bool


class DimTimeCreate(DimTimeBase):
    pass


class DimTimeUpdate(DimTimeBase):
    pass


class DimTimeOut(DimTimeBase):
    time_id: int

    class Config:
        from_attributes= True


# ---------- dim_tables ----------
class DimTableBase(BaseModel):
    nfc_wifi_tag: Optional[str]
    nfc_menu_tag: Optional[str]
    nfc_review_tag: Optional[str]


class DimTableCreate(DimTableBase):
    pass


class DimTableUpdate(DimTableBase):
    pass


class DimTableOut(DimTableBase):
    table_id: int

    class Config:
        from_attributes= True


# ---------- nfc_engagements ----------
class NfcEngagementBase(BaseModel):
    mobile_id: str
    table_id: int
    tag_type: str
    engagement_time: datetime


class NfcEngagementCreate(NfcEngagementBase):
    pass


class NfcEngagementUpdate(NfcEngagementBase):
    pass


class NfcEngagementOut(NfcEngagementBase):
    engagement_id: int

    class Config:
        from_attributes= True


# ---------- dim_menu_items ----------
class DimMenuItemBase(BaseModel):
    menu_item_name: str
    price: float
    category: str


class DimMenuItemCreate(DimMenuItemBase):
    pass


class DimMenuItemUpdate(DimMenuItemBase):
    pass


class DimMenuItemOut(DimMenuItemBase):
    item_id: int

    class Config:
        from_attributes= True


# ---- Auth ----
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---- Dashboard Overview ----
class DashboardOverview(BaseModel):
    total_sales: float
    total_transactions: int
    total_users: int
    total_items_sold: int
    last_updated: datetime


# ---- Sales Trend ----
class SalesTrendItem(BaseModel):
    date: date
    total_sales: float


class SalesTrendResponse(BaseModel):
    trend: List[SalesTrendItem]


# ---- NFC Engagement ----
class NfcEngagementStats(BaseModel):
    tag_type: str
    total_engagements: int


class NfcEngagementDashboardResponse(BaseModel):
    stats: List[NfcEngagementStats]
    last_updated: datetime
