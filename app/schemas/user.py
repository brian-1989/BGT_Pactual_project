from app.schemas.transaction import TransactionSchema
from app.schemas.funds import FundsSchema
from pydantic import BaseModel, Field
from typing import List

class UserSchema(BaseModel):
    _id: str
    name: str
    balance: int
    funds: List[FundsSchema]
    transactions: List[TransactionSchema]
