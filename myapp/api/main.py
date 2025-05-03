from database import get_db, engine
import schemas
import crud
import models
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


# Create DB tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# ========== Tables ==========

# ----------------- Transactions -----------------
@app.get("/api/transactions/", response_model=List[schemas.FactTransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return crud.crud_fact_transaction.get_multi(db)


# ----------------- Fact Transaction Items -----------------
@app.get("/api/fact_transaction_items/", response_model=List[schemas.FactTransactionItemOut])
def get_transaction_items(db: Session = Depends(get_db)):
    return crud.crud_fact_transaction_item.get_multi(db)


# ----------------- Dim Menu Daytimes -----------------
@app.get("/api/dim_menu_daytimes/", response_model=List[schemas.DimMenuDaytimeOut])
def get_menu_daytimes(db: Session = Depends(get_db)):
    return crud.crud_dim_menu_daytime.get_multi(db)


# ----------------- Menu Recommendations -----------------
@app.get("/api/menu_recommendations/", response_model=List[schemas.MenuRecommendationOut])
def get_menu_recommendations(db: Session = Depends(get_db)):
    return crud.crud_menu_recommendation.get_multi(db)


@app.post("/api/menu_recommendations/", response_model=schemas.MenuRecommendationOut)
def create_menu_recommendation(
    obj_in: schemas.MenuRecommendationCreate, db: Session = Depends(get_db)
):
    return crud.crud_menu_recommendation.create(db, obj_in=obj_in)


# ----------------- Users -----------------
@app.get("/api/users/", response_model=List[schemas.DimUserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.crud_dim_user.get_multi(db)


# ----------------- RFM Segments -----------------
@app.get("/api/rfm_segments/", response_model=List[schemas.RfmSegmentOut])
def get_rfm_segments(db: Session = Depends(get_db)):
    return crud.crud_rfm_segment.get_multi(db)


@app.post("/api/rfm_segments/", response_model=schemas.RfmSegmentOut)
def create_rfm_segment(
    obj_in: schemas.RfmSegmentCreate, db: Session = Depends(get_db)
):
    return crud.crud_rfm_segment.create(db, obj_in=obj_in)


# ----------------- Dashboard: Overview -----------------
@app.get("/api/dashboard/overview", response_model=schemas.DashboardOverview)
def dashboard_overview(db: Session = Depends(get_db)):
    total_sales = db.query(models.FactTransaction).with_entities(func.sum(models.FactTransaction.total_amount)).scalar() or 0
    total_transactions = db.query(models.FactTransaction).count()
    total_users = db.query(models.DimUser).count()
    total_items_sold = db.query(models.FactTransactionItem).with_entities(func.sum(models.FactTransactionItem.quantity)).scalar() or 0

    return schemas.DashboardOverview(
        total_sales=total_sales,
        total_transactions=total_transactions,
        total_users=total_users,
        total_items_sold=total_items_sold,
        last_updated=datetime.utcnow()
    )


# ----------------- Dashboard: Sales Trend -----------------
from sqlalchemy import func
from datetime import datetime

@app.get("/api/dashboard/sales_trend", response_model=schemas.SalesTrendResponse)
def sales_trend(db: Session = Depends(get_db)):
    sales_data = (
        db.query(models.DimTime.date, func.sum(models.FactTransaction.total_amount).label("total_sales"))
        .join(models.FactTransaction, models.DimTime.time_id == models.FactTransaction.time_id)
        .group_by(models.DimTime.date)
        .all()
    )
    trend = [schemas.SalesTrendItem(date=row[0], total_sales=row[1]) for row in sales_data]
    return schemas.SalesTrendResponse(trend=trend)


# ----------------- Dashboard: NFC Engagement -----------------
@app.get("/api/dashboard/nfc_engagement", response_model=schemas.NfcEngagementDashboardResponse)
def nfc_engagement_dashboard(db: Session = Depends(get_db)):
    data = (
        db.query(models.NfcEngagement.tag_type, func.count(models.NfcEngagement.engagement_id))
        .group_by(models.NfcEngagement.tag_type)
        .all()
    )
    stats = [
        schemas.NfcEngagementStats(tag_type=row[0], total_engagements=row[1]) for row in data
    ]
    return schemas.NfcEngagementDashboardResponse(
        stats=stats,
        last_updated=datetime.utcnow()
    )


# ----------------- Segments: RFM -----------------
@app.get("/api/segments/rfm", response_model=List[schemas.RfmSegmentOut])
def get_rfm_segments_list(db: Session = Depends(get_db)):
    return crud.crud_rfm_segment.get_multi(db)


# ----------------- Campaigns -----------------
@app.get("/api/campaigns/", response_model=List[schemas.MarketingCampaignOut])
def get_campaigns(db: Session = Depends(get_db)):
    return crud.crud_marketing_campaign.get_multi(db)


@app.post("/api/campaigns/", response_model=schemas.MarketingCampaignOut)
def create_campaign(
    obj_in: schemas.MarketingCampaignCreate, db: Session = Depends(get_db)
):
    return crud.crud_marketing_campaign.create(db, obj_in=obj_in)


# ----------------- Recommendations: Menu -----------------
@app.get("/api/recommendations/menu", response_model=List[schemas.MenuRecommendationOut])
def get_menu_recommendations_alt(db: Session = Depends(get_db)):
    return crud.crud_menu_recommendation.get_multi(db)


# ----------------- Auth: Login -----------------
@app.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(obj_in: schemas.LoginRequest):
    # Dummy auth logic - replace with real auth system
    if obj_in.username == "admin" and obj_in.password == "password":
        return schemas.TokenResponse(access_token="dummy-jwt-token")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
