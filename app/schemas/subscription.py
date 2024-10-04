from pydantic import BaseModel
from typing import Literal

class SubscriptionSchema(BaseModel):
    fund_id: str
    notification_type: Literal["email", "sms"]
