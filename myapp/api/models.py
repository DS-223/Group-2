# models.py

"""
SQLAlchemy ORM models for the application's PostgreSQL database.

These models define the structure of fact and dimension tables used for transactional,
user, time, and campaign data in a restaurant analytics platform.
"""

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Time, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # Assuming you have Base from declarative_base()

# ---------- Fact Transactions ----------
class FactTransaction(Base):
    """
    Fact table storing transactional sales data.

    Columns:
    - transaction_id: Unique transaction identifier
    - mobile_id: Foreign key to user (dim_users)
    - table_id: Foreign key to table (dim_tables)
    - time_id: Foreign key to time (dim_time)
    - total_amount: Total value of the transaction
    - created_at: Timestamp of transaction creation

    Relationships:
    - items: List of items in the transaction
    - user: Associated user (DimUser)
    """
    __tablename__ = "fact_transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    mobile_id = Column(String, ForeignKey("dim_users.mobile_id"))
    table_id = Column(Integer, ForeignKey("dim_tables.table_id"))
    time_id = Column(Integer, ForeignKey("dim_time.time_id"))
    total_amount = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    items = relationship("FactTransactionItem", back_populates="transaction")
    user = relationship("DimUser", back_populates="transactions")


# ---------- Fact Transaction Items ----------
class FactTransactionItem(Base):
    """
    Line items for each transaction, specifying product-level details.

    Columns:
    - id: Primary key
    - transaction_id: Foreign key to fact_transactions
    - item_id: Foreign key to menu item
    - quantity: Number of items ordered
    - price: Price per unit

    Relationships:
    - transaction: Associated transaction
    - menu_item: Associated menu item
    """
    __tablename__ = "fact_transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("fact_transactions.transaction_id"))
    item_id = Column(Integer, ForeignKey("dim_menu_items.item_id"))
    quantity = Column(Integer)
    price = Column(Float)

    transaction = relationship("FactTransaction", back_populates="items")
    menu_item = relationship("DimMenuItem")


# ---------- Dim Menu Daytimes ----------
class DimMenuDaytime(Base):
    """
    Dimension table for defining time-based menu segments (e.g., Breakfast, Lunch).

    Columns:
    - daytime_id: Unique ID
    - daytime_label: Label (e.g., 'Lunch')
    - start_time: Start time of this daytime
    - end_time: End time of this daytime
    """
    __tablename__ = "dim_menu_daytimes"

    daytime_id = Column(Integer, primary_key=True, index=True)
    daytime_label = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)


# ---------- Menu Recommendations ----------
class MenuRecommendation(Base):
    """
    Stores ranked menu item recommendations for different dayparts.

    Columns:
    - id: Primary key
    - menu_item_id: Foreign key to DimMenuItem
    - daytime_id: Foreign key to DimMenuDaytime
    - rank: Rank position in recommendation

    Relationships:
    - menu_item: The recommended menu item
    - daytime: Time of day this recommendation applies to
    """
    __tablename__ = "menu_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("dim_menu_items.item_id"))
    daytime_id = Column(Integer, ForeignKey("dim_menu_daytimes.daytime_id"))
    rank = Column(Integer)

    menu_item = relationship("DimMenuItem")
    daytime = relationship("DimMenuDaytime")


# ---------- Dim Users ----------
class DimUser(Base):
    """
    Dimension table containing user information.

    Columns:
    - mobile_id: Unique user identifier (e.g., phone number)
    - notes: Optional notes about the user

    Relationships:
    - transactions: List of transactions by user
    - engagements: NFC tag engagements
    - rfm_segments: RFM segmentation history
    """
    __tablename__ = "dim_users"

    mobile_id = Column(String, primary_key=True, index=True)
    notes = Column(Text, nullable=True)

    transactions = relationship("FactTransaction", back_populates="user")
    engagements = relationship("NfcEngagement", back_populates="user")
    rfm_segments = relationship("RfmSegment", back_populates="user")


# ---------- RFM Segments ----------
class RfmSegment(Base):
    """
    Stores RFM segmentation scores for each user.

    Columns:
    - rfm_id: Primary key
    - mobile_id: Foreign key to DimUser
    - recency_days: Days since last transaction
    - frequency: Number of transactions
    - monetary: Total spend
    - R_score, F_score, M_score: Individual scores
    - RFM_score: Composite score string (e.g., '532')
    - segment: Assigned segment label
    - date_created: Timestamp when segment was assigned

    Relationships:
    - user: Associated user
    """
    __tablename__ = "rfm_segments"

    rfm_id = Column(Integer, primary_key=True, index=True)
    mobile_id = Column(String, ForeignKey("dim_users.mobile_id"))
    recency_days = Column(Integer)
    frequency = Column(Integer)
    monetary = Column(Float)
    R_score = Column(Integer)
    F_score = Column(Integer)
    M_score = Column(Integer)
    RFM_score = Column(String)
    segment = Column(String)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("DimUser", back_populates="rfm_segments")


# ---------- Marketing Campaigns ----------
class MarketingCampaign(Base):
    """
    Campaign metadata for marketing efforts targeting RFM segments.

    Columns:
    - campaign_id: Unique campaign ID
    - name: Campaign name
    - start_time_id, end_time_id: Foreign keys to DimTime
    - target_segment: Target RFM segment
    - description: Campaign details

    Relationships:
    - start_time, end_time: Campaign duration info
    """
    __tablename__ = "marketing_campaigns"

    campaign_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_time_id = Column(Integer, ForeignKey("dim_time.time_id"))
    end_time_id = Column(Integer, ForeignKey("dim_time.time_id"))
    target_segment = Column(String)
    description = Column(Text, nullable=True)

    start_time = relationship("DimTime", foreign_keys=[start_time_id])
    end_time = relationship("DimTime", foreign_keys=[end_time_id])


# ---------- Dim Time ----------
class DimTime(Base):
    """
    Time dimension table used for filtering and grouping by time components.

    Columns:
    - time_id: Primary key
    - date: Full date
    - day_of_week: String name of the day
    - month: Month number
    - year: Year
    - is_weekend: Boolean flag
    """
    __tablename__ = "dim_time"

    time_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    day_of_week = Column(String)
    month = Column(Integer)
    year = Column(Integer)
    is_weekend = Column(Boolean)


# ---------- Dim Tables ----------
class DimTable(Base):
    """
    Table dimension mapping NFC tags to physical tables.

    Columns:
    - table_id: Primary key
    - nfc_wifi_tag, nfc_menu_tag, nfc_review_tag: NFC tag types
    """
    __tablename__ = "dim_tables"

    table_id = Column(Integer, primary_key=True, index=True)
    nfc_wifi_tag = Column(String, nullable=True)
    nfc_menu_tag = Column(String, nullable=True)
    nfc_review_tag = Column(String, nullable=True)


# ---------- NFC Engagements ----------
class NfcEngagement(Base):
    """
    Records NFC interactions by users at different tables.

    Columns:
    - engagement_id: Primary key
    - mobile_id: Foreign key to user
    - table_id: Foreign key to table
    - tag_type: Type of NFC tag engaged with
    - engagement_time: Timestamp

    Relationships:
    - user: The engaged user
    - table: The table interacted with
    """
    __tablename__ = "nfc_engagements"

    engagement_id = Column(Integer, primary_key=True, index=True)
    mobile_id = Column(String, ForeignKey("dim_users.mobile_id"))
    table_id = Column(Integer, ForeignKey("dim_tables.table_id"))
    tag_type = Column(String)
    engagement_time = Column(DateTime)

    user = relationship("DimUser", back_populates="engagements")
    table = relationship("DimTable")


# ---------- Dim Menu Items ----------
class DimMenuItem(Base):
    """
    Menu item dimension storing item metadata.

    Columns:
    - item_id: Primary key
    - menu_item_name: Name of the menu item
    - price: Price
    - category: Food or drink category
    """
    __tablename__ = "dim_menu_items"

    item_id = Column(Integer, primary_key=True, index=True)
    menu_item_name = Column(String)
    price = Column(Float)
    category = Column(String)
