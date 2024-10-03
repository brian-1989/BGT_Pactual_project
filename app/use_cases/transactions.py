from app.database import Transactions
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class FundTransactionsUseCase:

    def execute(self):
        try:
            all_transactions = []
            for transaction in Transactions.find():
                id_value = transaction["_id"]
                date_value = transaction.get("created_at")
                transaction.update(
                    {
                        "created_at": str(date_value.strftime("%Y-%m-%d")),
                        "_id": str(id_value)
                })
                all_transactions.append(transaction)
            return JSONResponse(
                jsonable_encoder(all_transactions),
                status_code=status.HTTP_200_OK
            )
        except Exception as error:
            return JSONResponse(
                jsonable_encoder(
                    {"error_message": str(error)}
                ),
                status_code=status.HTTP_400_BAD_REQUEST
            )
