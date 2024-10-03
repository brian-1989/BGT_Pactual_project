from app.database import Funds, Users, Transactions
from app.serializer import serializerTransaction
from app.translation import error_translation, success_translation
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# FALTA HACER EL ENVIO DE CORREO O SMS

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
            # Check if the user is subscribed to the fund
            subscription = Transactions.find_one(
                {
                    "fund_id": fund_id,
                    "transaction_type": "subscription"
                }
            )
            if subscription:
                raise Exception(
                    error_translation.get(
                        "subscribed_to_the_fund"
                    ).format(get_user.get("name"), get_fund.get("name"))
                )
            # Validate if there is available balance to subscribe to the fund
            if get_user.get("balance") < get_fund.get("minimum_amount"):
                raise Exception(
                    error_translation.get(
                        "minimum_amount_not_sufficient"
                    ).format(get_fund.get("name"))
                )
            # Create a subscription transaction
            transaction = serializerTransaction(
                fund=get_fund,
                transaction_type="subscription"
            )
            # Update user balance
            new_amount = get_user.get("balance") - get_fund.get("minimum_amount")
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
                status_code=status.HTTP_201_CREATED
            )
        except Exception as error:
            return JSONResponse(
                jsonable_encoder(
                    {"error_message": str(error)}
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
