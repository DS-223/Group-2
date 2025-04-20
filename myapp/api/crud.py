from data_access import CRUDBase
from models import DimTable, DimTime, FactTransaction, MarketingCampaign

table_crud = CRUDBase(DimTable)
time_crud = CRUDBase(DimTime)
transaction_crud = CRUDBase(FactTransaction)
campaign_crud = CRUDBase(MarketingCampaign)
