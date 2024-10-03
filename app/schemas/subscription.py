from pydantic import BaseModel

class SubscriptionSchema(BaseModel):
    fund_id: str
    amount: int
    notification_type: str
