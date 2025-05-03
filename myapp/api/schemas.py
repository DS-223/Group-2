"""
Pydantic schemas used for API input/output models.

These schemas define the data structure exchanged between the backend and client,
ensuring validation, serialization, and consistency across routes.
"""
from datetime import date, datetime, time
from typing import Optional, List
from pydantic import BaseModel


# ---------- fact_transactions ----------
class FactTransactionBase(BaseModel):
    """Base schema for fact_transactions table."""
    mobile_id: str
    table_id: int
    time_id: int
    total_amount: float


class FactTransactionCreate(FactTransactionBase):
    """Schema for creating a new transaction."""
    pass


class FactTransactionUpdate(FactTransactionBase):
    """Schema for updating an existing transaction."""
    pass


class FactTransactionOut(FactTransactionBase):
    """Schema for returning transaction data to client."""
    transaction_id: int
    created_at: datetime

    class Config:
        from_attributes= True


# ---------- fact_transaction_items ----------
class FactTransactionItemBase(BaseModel):
    """Base schema for fact_transaction_items table."""
    transaction_id: int
    item_id: int
    quantity: int
    price: float


class FactTransactionItemCreate(FactTransactionItemBase):
    """Schema for creating a new transaction item."""
    pass


class FactTransactionItemUpdate(FactTransactionItemBase):
    """Schema for updating a transaction item."""
    pass


class FactTransactionItemOut(FactTransactionItemBase):
    """Schema for returning transaction item data to client."""
    class Config:
        from_attributes= True


# ---------- dim_menu_daytimes ----------
class DimMenuDaytimeBase(BaseModel):
    """Base schema for dim_menu_daytimes table."""
    daytime_label: str
    start_time: time
    end_time: time


class DimMenuDaytimeCreate(DimMenuDaytimeBase):
    """Schema for creating a new daytime record."""
    pass


class DimMenuDaytimeUpdate(DimMenuDaytimeBase):
    """Schema for updating a daytime record."""
    pass


class DimMenuDaytimeOut(DimMenuDaytimeBase):
    """Schema for returning daytime record to client."""
    daytime_id: int

    class Config:
        from_attributes= True


# ---------- menu_recommendations ----------
class MenuRecommendationBase(BaseModel):
    """Base schema for menu_recommendations table."""
    menu_item_id: int
    daytime_id: int
    rank: int


class MenuRecommendationCreate(MenuRecommendationBase):
    """Schema for creating a new menu recommendation."""


class MenuRecommendationUpdate(MenuRecommendationBase):
    """Schema for updating a menu recommendation."""


class MenuRecommendationOut(MenuRecommendationBase):
    """Schema for returning a menu recommendation."""
    id: int

    class Config:
        from_attributes= True


# ---------- dim_users ----------
class DimUserBase(BaseModel):
    """Base schema for dim_users table."""
    notes: Optional[str] = None


class DimUserCreate(DimUserBase):
    """Schema for creating a new user."""
    mobile_id: str


class DimUserUpdate(DimUserBase):
    """Schema for updating user notes."""
    pass


class DimUserOut(DimUserBase):
    """Schema for returning user information to client."""
    mobile_id: str

    class Config:
        from_attributes= True


# ---------- rfm_segments ----------
class RfmSegmentBase(BaseModel):
    """Base schema for rfm_segments table."""
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
    """Schema for creating RFM segment entry."""
    pass


class RfmSegmentUpdate(RfmSegmentBase):
    """Schema for updating RFM segment entry."""
    pass


class RfmSegmentOut(RfmSegmentBase):
    """Schema for returning RFM segment data."""
    rfm_id: int
    date_created: datetime

    class Config:
        from_attributes= True


# ---------- marketing_campaigns ----------
class MarketingCampaignBase(BaseModel):
    """Base schema for marketing_campaigns table."""
    name: str
    start_time_id: int
    end_time_id: int
    target_segment: str
    description: Optional[str] = None


class MarketingCampaignCreate(MarketingCampaignBase):
    """Schema for creating a marketing campaign."""
    pass


class MarketingCampaignUpdate(MarketingCampaignBase):
    """Schema for updating a marketing campaign."""
    pass


class MarketingCampaignOut(MarketingCampaignBase):
    """Schema for returning campaign data."""
    campaign_id: int

    class Config:
        from_attributes= True


# ---------- dim_time ----------
class DimTimeBase(BaseModel):
    """Base schema for dim_time table."""
    date: date
    day_of_week: str
    month: int
    year: int
    is_weekend: bool


class DimTimeCreate(DimTimeBase):
    """Schema for creating a time record."""
    pass


class DimTimeUpdate(DimTimeBase):
    """Schema for updating a time record."""
    pass


class DimTimeOut(DimTimeBase):
    """Schema for returning time record."""
    time_id: int

    class Config:
        from_attributes= True


# ---------- dim_tables ----------
class DimTableBase(BaseModel):
    """Base schema for dim_tables table."""
    nfc_wifi_tag: Optional[str]
    nfc_menu_tag: Optional[str]
    nfc_review_tag: Optional[str]


class DimTableCreate(DimTableBase):
    """Schema for creating a table entry."""
    pass


class DimTableUpdate(DimTableBase):
    """Schema for updating table metadata."""
    pass


class DimTableOut(DimTableBase):
    """Schema for returning table metadata."""
    table_id: int

    class Config:
        from_attributes= True


# ---------- nfc_engagements ----------
class NfcEngagementBase(BaseModel):
    """Base schema for nfc_engagements table."""
    mobile_id: str
    table_id: int
    tag_type: str
    engagement_time: datetime


class NfcEngagementCreate(NfcEngagementBase):
    """Schema for creating NFC engagement."""
    pass


class NfcEngagementUpdate(NfcEngagementBase):
    """Schema for updating NFC engagement."""
    pass


class NfcEngagementOut(NfcEngagementBase):
    """Schema for returning NFC engagement data."""
    engagement_id: int

    class Config:
        from_attributes= True


# ---------- dim_menu_items ----------
class DimMenuItemBase(BaseModel):
    """Base schema for dim_menu_items table."""
    menu_item_name: str
    price: float
    category: str


class DimMenuItemCreate(DimMenuItemBase):
    """Schema for creating a new menu item."""
    pass


class DimMenuItemUpdate(DimMenuItemBase):
    """Schema for updating a menu item."""
    pass


class DimMenuItemOut(DimMenuItemBase):
    """Schema for returning menu item data."""
    item_id: int

    class Config:
        from_attributes= True


# ---- Auth ----
class LoginRequest(BaseModel):
    """Schema for login credentials."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


# ---- Dashboard Overview ----
class DashboardOverview(BaseModel):
    """Schema for top-level dashboard metrics."""
    total_sales: float
    total_transactions: int
    total_users: int
    total_items_sold: int
    last_updated: datetime


# ---- Sales Trend ----
class SalesTrendItem(BaseModel):
    """Single time point in sales trend line chart."""
    date: date
    total_sales: float


class SalesTrendResponse(BaseModel):
    """Sales trend over time."""
    trend: List[SalesTrendItem]


# ---- NFC Engagement ----
class NfcEngagementStats(BaseModel):
    """Engagement count per NFC tag type."""
    tag_type: str
    total_engagements: int


class NfcEngagementDashboardResponse(BaseModel):
    """Dashboard response for NFC engagement analytics."""
    stats: List[NfcEngagementStats]
    last_updated: datetime
