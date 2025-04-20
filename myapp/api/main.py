from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import crud

app = FastAPI()

# ========== Tables ==========

@app.post("/tables/", response_model=schemas.DimTableOut)
def create_table(table: schemas.DimTableCreate, db: Session = Depends(get_db)):
    return crud.table_crud.create(db, table.dict())

@app.get("/tables/", response_model=list[schemas.DimTableOut])
def get_tables(db: Session = Depends(get_db)):
    return crud.table_crud.get_all(db)

@app.get("/tables/{table_id}", response_model=schemas.DimTableOut)
def get_table(table_id: int, db: Session = Depends(get_db)):
    result = crud.table_crud.get(db, table_id)
    if not result:
        raise HTTPException(status_code=404, detail="Table not found")
    return result

@app.delete("/tables/{table_id}", response_model=schemas.DimTableOut)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    obj = crud.table_crud.delete(db, table_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Table not found")
    return obj

# ========== Time ==========

@app.get("/time/", response_model=list[schemas.DimTimeOut])
def get_all_time(db: Session = Depends(get_db)):
    return crud.time_crud.get_all(db)

# ========== Transactions ==========

@app.get("/transactions/", response_model=list[schemas.FactTransactionOut])
def get_transactions(db: Session = Depends(get_db)):
    return crud.transaction_crud.get_all(db)

# ========== Marketing Campaigns ==========

@app.get("/campaigns/", response_model=list[schemas.MarketingCampaignOut])
def get_campaigns(db: Session = Depends(get_db)):
    return crud.campaign_crud.get_all(db)

@app.get("/users/", response_model=list[schemas.DimUserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.user_crud.get_all(db)