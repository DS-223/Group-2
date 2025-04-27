from data_access import CRUDBase
from models import DimTable, DimTime, FactTransaction, MarketingCampaign, DimUser, RFMResult

table_crud = CRUDBase(DimTable)
time_crud = CRUDBase(DimTime)
transaction_crud = CRUDBase(FactTransaction)
campaign_crud = CRUDBase(MarketingCampaign)
user_crud = CRUDBase(DimUser)
rfm_result_crud = CRUDBase(RFMResult)
