from app.database import db
from app.schemas.cancellation import CancellationSchema
from app.use_cases.cancellation import CancelFundUseCase
from fastapi import APIRouter

router = APIRouter()

@router.post("/cancel_fund")
def cancellation_fund(cancel: CancellationSchema):
    fund_id = cancel.fund_id
    uc = CancelFundUseCase()
    return uc.execute(
        fund_id=fund_id
    )
