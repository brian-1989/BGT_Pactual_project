from app.config import Settings
from app.database import Funds, Users, Transactions
from app.serializer import serializerTransaction
from app.translation import (
    error_translation,
    success_translation,
    email_translation
)
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from email.message import EmailMessage
import smtplib
import ssl
import vonage


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
                    "transaction_type": "subscription",
                    "status": "active",
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
            new_amount = get_user.get("balance") - \
                get_fund.get("minimum_amount")
            Users.find_one_and_update(
                {"_id": "1"}, {"$set": {"balance": new_amount}})
            # Record transaction
            Transactions.insert_one(transaction)
            # Send notification via Email or SMS
            if notification_type == "email":
                self.send_to_email(
                    receiver_email=get_user.get("email"),
                    fund_name=get_fund.get("name")
                )
            else:
                self.send_to_sms(
                    cellphone=get_user.get("cellphone"),
                    fund_name=get_fund.get("name")
                )
            # Successful response
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

    def send_to_email(self, receiver_email: str, fund_name: str):
        # Port for SSL
        port = Settings.SMTP_PORT
        # Smtp mail server that uses gmail mail
        smtp_server = Settings.SMTP_SERVER
        # Sender email
        sender_email = Settings.SENDER_EMAIL
        # App password
        password = Settings.PASSWORD_EMAIL
        # Create email
        message = EmailMessage()
        message['Subject'] = email_translation.get(
            "successful_subscription")
        message['From'] = sender_email
        message['To'] = receiver_email
        # Message body
        message.set_content(
            email_translation.get(
                "message_body"
            ).format(fund_name)
        )
        # Send to email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            smtp_server, port=port, context=context
        ) as server_connection:
            server_connection.login(sender_email, password)
            server_connection.send_message(message)

    def send_to_sms(self, cellphone: str, fund_name: str):
        # Vonage credentials
        client = vonage.Client(
            key=Settings.VONAGE_KEY,
            secret=Settings.VONAGE_SECRET
        )
        # Send to sms
        sms = vonage.Sms(client)
        sms.send_message(
            {
                "from": "BGT Pactual",
                "to": cellphone,
                "text": email_translation.get(
                    "message_body"
                ).format(fund_name)
            }
        )
