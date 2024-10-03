from app.database import db
from app.schemas.subscription import SubscriptionSchema
from app.use_cases.subscription import SubscriptionFundUseCase
from fastapi import APIRouter

router = APIRouter()

@router.post("/subscribe_fund")
def subscribe_fund(subscription: SubscriptionSchema):
    fund_id = subscription.fund_id
    notification_type = subscription.notification_type
    uc = SubscriptionFundUseCase()
    return uc.execute(
        fund_id=fund_id,
        notification_type=notification_type
    )
