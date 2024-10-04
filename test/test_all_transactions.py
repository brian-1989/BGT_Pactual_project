from app.use_cases.transactions import FundTransactionsUseCase
from fastapi import status
import json

class TestAllTransactions:

    def test_successful_all_transactions(self, mocker):
        mock_all_transactions = mocker.patch('app.database.Transactions.find')

        all_transactions = [
            {
                "_id": "66ff320bfa3ecb902165fdd9",
                "transaction_id": "123",
                "fund_id": "1",
                "fund_name": "Fund Test",
                "transaction_type": "subscription",
                "amount": 100,
                "status": "active",
                "created_at": mocker.Mock(strftime=lambda x: "2023-10-01")
            },
            {
                "_id": "66ff30b670fb973320e75eb0",
                "transaction_id": "123",
                "fund_id": "1",
                "fund_name": "Fund Test",
                "transaction_type": "subscription",
                "amount": 100,
                "status": "inactive",
                "created_at": mocker.Mock(strftime=lambda x: "2023-10-02")
            }
        ]

        mock_all_transactions.return_value = all_transactions

        use_case = FundTransactionsUseCase()

        response = use_case.execute()
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_200_OK
        assert response_json == all_transactions
