from sqlalchemy import Column, Integer, Numeric, String, Date, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import engine

Base = declarative_base()

class FactTransaction(Base):
    __tablename__ = "fact_transactions"
    transaction_id = Column(Integer, primary_key=True)
    table_id       = Column(Integer, ForeignKey("dim_tables.table_id"), nullable=False)
    time_id        = Column(Integer, ForeignKey("dim_time.time_id"), nullable=False)
    total_amount   = Column(Numeric)
    created_at     = Column(TIMESTAMP)

    table = relationship("DimTable", back_populates="transactions")
    time  = relationship("DimTime",  back_populates="transactions")
    items = relationship("FactTransactionItem", back_populates="transaction")

class FactTransactionItem(Base):
    __tablename__ = "fact_transaction_items"
    transaction_id = Column(Integer, ForeignKey("fact_transactions.transaction_id"), primary_key=True)
    item_id        = Column(Integer, ForeignKey("dim_menu_items.item_id"), primary_key=True)
    quantity       = Column(Integer)
    price          = Column(Numeric) 

    transaction = relationship("FactTransaction", back_populates="items")
    item        = relationship("DimMenuItem", back_populates="transaction_items")

class DimTable(Base):
    __tablename__ = "dim_tables"
    table_id       = Column(Integer, primary_key=True)
    nfc_wifi_tag   = Column(String)
    nfc_menu_tag   = Column(String)
    nfc_review_tag = Column(String)

    transactions = relationship("FactTransaction", back_populates="table")
    engagements  = relationship("NfcEngagement",  back_populates="table")

class DimTime(Base):
    __tablename__ = "dim_time"
    time_id     = Column(Integer, primary_key=True)
    date        = Column(Date)
    day_of_week = Column(String)
    month       = Column(Integer)
    year        = Column(Integer)
    is_weekend  = Column(Boolean)

    transactions     = relationship("FactTransaction", back_populates="time")
    marketing_starts = relationship(
        "MarketingCampaign",
        back_populates="start_time",
        foreign_keys="[MarketingCampaign.start_time_id]"
    )
    marketing_ends   = relationship(
        "MarketingCampaign",
        back_populates="end_time",
        foreign_keys="[MarketingCampaign.end_time_id]"
    )

class DimMenuItem(Base):
    __tablename__ = "dim_menu_items"
    item_id     = Column(Integer, primary_key=True)
    item_name   = Column(String)
    price       = Column(Numeric)
    category    = Column(String)

    transaction_items = relationship("FactTransactionItem", back_populates="item")

class NfcEngagement(Base):
    __tablename__ = "nfc_engagements"
    engagement_id   = Column(Integer, primary_key=True)
    table_id        = Column(Integer, ForeignKey("dim_tables.table_id"), nullable=False)
    tag_type        = Column(String)  
    mobile_id       = Column(String, comment="Hashed/anonymous device identifier")
    engagement_time = Column(TIMESTAMP)

    table = relationship("DimTable", back_populates="engagements")

class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    campaign_id    = Column(Integer, primary_key=True)
    name           = Column(String)
    start_time_id  = Column(Integer, ForeignKey("dim_time.time_id"), nullable=False)
    end_time_id    = Column(Integer, ForeignKey("dim_time.time_id"), nullable=False)
    target_segment = Column(String)
    description    = Column(Text)

    start_time = relationship(
        "DimTime",
        back_populates="marketing_starts",
        foreign_keys=[start_time_id]
    )
    end_time   = relationship(
        "DimTime",
        back_populates="marketing_ends",
        foreign_keys=[end_time_id]
    )

Base.metadata.create_all(bind=engine)