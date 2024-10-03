from app.utils import create_date
from uuid import uuid4

def serializerTransaction(fund: dict, transaction_type: str) -> dict:
    status = "active" if transaction_type == "subscription"\
        else "inactive"
    transaction = {
        "transaction_id": str(uuid4()),
        "fund_id": str(fund.get("_id")),
        "fund_name": fund.get("name"),
        "transaction_type": transaction_type,
        "amount": fund.get("minimum_amount"),
        "status": status,
        "created_at": create_date()
    }
    return transaction