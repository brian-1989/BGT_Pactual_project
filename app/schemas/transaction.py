from datetime import datetime
from pydantic import BaseModel

class TransactionSchema(BaseModel):
    transaction_id: str
    type: str
    fund_id: str
    amount: int
    created_at: datetime
