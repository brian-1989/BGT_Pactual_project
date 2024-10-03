from app.use_cases.transactions import FundTransactionsUseCase
from fastapi import APIRouter

router = APIRouter()

@router.get("/all_transactions")
def all_transactions():
    uc = FundTransactionsUseCase()
    return uc.execute()
