from app.database import Funds, Users, Transactions
from app.serializer import serializerTransaction
from app.translation import error_translation, success_translation
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class CancelFundUseCase:

    def __init__(self) -> None:
        pass

    def execute(self, fund_id: int):
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
            # Check if the user has already canceled the
            # subscription to the fund
            inactive_subscription = Transactions.find_one(
                {
                    "fund_id": fund_id,
                    "transaction_type": "cancellation"
                }
            )
            if inactive_subscription:
                raise Exception(
                    error_translation.get(
                        "canceled_the_subscription"
                    ).format(get_user.get("name"), get_fund.get("name"))
                )
            # Check if the user has an active subscription to the fund
            active_subscription = Transactions.find_one(
                {
                    "fund_id": fund_id,
                    "transaction_type": "subscription",
                    "status": "active"
                }
            )
            if not active_subscription:
                raise Exception(
                    error_translation.get(
                        "not_subscribed_to_the_fund"
                    ).format(get_user.get("name"), get_fund.get("name"))
                )
            # Create a cancellation transaction
            transaction = serializerTransaction(
                fund=get_fund,
                transaction_type="cancellation"
            )
            # Update user balance
            new_amount = get_user.get("balance") + \
                active_subscription["amount"]
            Users.find_one_and_update(
                {"_id": "1"}, {"$set": {"balance": new_amount}})
            # Record transaction
            Transactions.insert_one(transaction)
            # Update subscription status
            Transactions.find_one_and_update(
                {"_id": active_subscription.get("_id")},
                {"$set": {"status": "inactive"}})
            # Success response
            success_message = success_translation.get(
                "cancel_subscription"
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
