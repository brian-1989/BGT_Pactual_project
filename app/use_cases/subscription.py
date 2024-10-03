from app.database import Funds, Users, Transactions
from app.translation import error_translation, success_translation
from datetime import datetime
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import uuid4
import pytz

class SubscriptionFundUseCase:

    def __init__(self) -> None:
        pass

    def execute(self, fund_id: int, notification_type: str):
        try:
            # Get if the fund exists
            get_fund = Funds.find_one({"_id": fund_id})
            if not get_fund:
                raise Exception(
                    error_translation.get("fund_not_found"))
            # Get user information
            get_user = Users.find_one()
            if not get_user:
                raise Exception(
                    error_translation.get("user_not_found"))
            # Validate if there is available balance to subscribe to the fund
            if get_user.get("balance") < get_fund.get("minimum_amount"):
                raise Exception(
                    error_translation.get(
                        "minimum_amount_not_sufficient"
                    ).format(get_fund.get("name"))
                )
            # Create transaction
            transaction = self.generate_transaction_structure(get_fund)
            # Update user balance
            new_amount = get_user["balance"] - get_fund["minimum_amount"]
            Users.find_one_and_update({"_id": "1"}, {"$set": {"balance": new_amount}})
            # Record transaction
            Transactions.insert_one(transaction)
            success_message = success_translation.get(
                "successful_subscription"
            ).format(get_fund.get("name"), new_amount)
            return JSONResponse(
                jsonable_encoder(
                    {"success_message": str(success_message)}
                ),
                status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return JSONResponse(
                jsonable_encoder(
                    {"error_message": str(error)}
                ),
                status_code=status.HTTP_400_BAD_REQUEST)

    def generate_transaction_structure(self, fund: dict) -> dict:
        transaction = {
            "transaction_id": str(uuid4()),
            "fund_id": str(fund.get("_id")),
            "fund_name": fund.get("name"),
            "transaction_type": "subscription",
            "amount": fund.get("minimum_amount"),
            "created_at": self.create_date()
        }
        return transaction

    def create_date(self):
        bogota_tz = pytz.timezone('America/Bogota')
        now = datetime.now(bogota_tz)
        return now
