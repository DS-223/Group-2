# models.py

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Time, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # Assuming you have Base from declarative_base()

# ---------- Fact Transactions ----------
class FactTransaction(Base):
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
    __tablename__ = "dim_menu_daytimes"

    daytime_id = Column(Integer, primary_key=True, index=True)
    daytime_label = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)


# ---------- Menu Recommendations ----------
class MenuRecommendation(Base):
    __tablename__ = "menu_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("dim_menu_items.item_id"))
    daytime_id = Column(Integer, ForeignKey("dim_menu_daytimes.daytime_id"))
    rank = Column(Integer)

    menu_item = relationship("DimMenuItem")
    daytime = relationship("DimMenuDaytime")


# ---------- Dim Users ----------
class DimUser(Base):
    __tablename__ = "dim_users"

    mobile_id = Column(String, primary_key=True, index=True)
    notes = Column(Text, nullable=True)

    transactions = relationship("FactTransaction", back_populates="user")
    engagements = relationship("NfcEngagement", back_populates="user")
    rfm_segments = relationship("RfmSegment", back_populates="user")


# ---------- RFM Segments ----------
class RfmSegment(Base):
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
    __tablename__ = "dim_time"

    time_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    day_of_week = Column(String)
    month = Column(Integer)
    year = Column(Integer)
    is_weekend = Column(Boolean)


# ---------- Dim Tables ----------
class DimTable(Base):
    __tablename__ = "dim_tables"

    table_id = Column(Integer, primary_key=True, index=True)
    nfc_wifi_tag = Column(String, nullable=True)
    nfc_menu_tag = Column(String, nullable=True)
    nfc_review_tag = Column(String, nullable=True)


# ---------- NFC Engagements ----------
class NfcEngagement(Base):
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
    __tablename__ = "dim_menu_items"

    item_id = Column(Integer, primary_key=True, index=True)
    menu_item_name = Column(String)
    price = Column(Float)
    category = Column(String)
