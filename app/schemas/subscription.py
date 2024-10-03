from pydantic import BaseModel

class SubscriptionSchema(BaseModel):
    fund_id: str
    notification_type: str
