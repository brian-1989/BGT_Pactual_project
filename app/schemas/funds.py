from pydantic import BaseModel

class FundsSchema(BaseModel):
    _id: str
    name: str
    minimum_amount: int
    category: str
