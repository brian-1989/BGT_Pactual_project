from app.use_cases.cancellation import CancelFundUseCase
from fastapi import status
import json

class TestForFundCancellation:

    def test_successful_cancellation(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')
        mock_serializer = mocker.patch('app.serializer.serializerTransaction')

        mocker.patch('app.database.Users.find_one_and_update')
        mocker.patch('app.database.Transactions.insert_one')
        mocker.patch('app.database.Transactions.find_one_and_update')

        fund_data = {
            "_id": 1,
            "name": "Fund Test",
            "minimum_amount": 100
        }
        user_data = {
            "_id": "1",
            "name": "Test Test",
            "balance": 200,
            "email": "test@test.com",
            "cellphone": "1234567890"
        }
        transaction_data = {
            "transaction_id": "123",
            "fund_id": "1",
            "fund_name": "Tech Fund",
            "transaction_type": "subscription",
            "amount": 100,
            "status": "active"
        }
        mocker.patch(
            'app.database.Transactions.find_one',
            side_effect=[None, transaction_data]
        )

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data
        mock_serializer.return_value = transaction_data

        use_case = CancelFundUseCase()

        response = use_case.execute(fund_id=1)
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_201_CREATED
        assert response_json == {
                'success_message': 'La cancelación de la suscripción al fondo Fund Test fue completada. El nuevo monto es de 300'
        }

    def test_failed_successful_cancellation_by_not_fund(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')

        mock_funds.return_value = None

        use_case = CancelFundUseCase()

        response = use_case.execute(fund_id=1)
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {'error_message': 'El fondo no fue encontrado'}

    def test_failed_successful_cancellation_by_not_user(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')

        fund_data = {
            "_id": 1,
            "name": "Fund Test",
            "minimum_amount": 100
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = None

        use_case = CancelFundUseCase()

        response = use_case.execute(fund_id=1)
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {'error_message': 'El usuario no fue encontrado'}

    def test_failed_successful_cancellation_by_inactive_subscrition(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')
        mock_inactive_subscription = mocker.patch(
            'app.database.Transactions.find_one'
        )

        fund_data = {
            "_id": 1,
            "name": "Fund Test",
            "minimum_amount": 100
        }
        user_data = {
            "_id": "1",
            "name": "Test Test",
            "balance": 200,
            "email": "test@test.com",
            "cellphone": "1234567890"
        }
        transaction_data = {
            "transaction_id": "123",
            "fund_id": "1",
            "fund_name": "Tech Fund",
            "transaction_type": "cancellation",
            "amount": 100,
            "status": "inactive"
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data
        mock_inactive_subscription.return_value = transaction_data

        use_case = CancelFundUseCase()

        response = use_case.execute(fund_id=1)
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {
            'error_message': 'El usario Test Test ya ha cancelado la suscripción al fondo Fund Test'
        }

    def test_failed_successful_cancellation_by_not_active_subscrition(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')

        mocker.patch('app.database.Users.find_one_and_update')
        mocker.patch('app.database.Transactions.insert_one')
        mocker.patch('app.database.Transactions.find_one_and_update')

        fund_data = {
            "_id": 1,
            "name": "Fund Test",
            "minimum_amount": 100
        }
        user_data = {
            "_id": "1",
            "name": "Test Test",
            "balance": 200,
            "email": "test@test.com",
            "cellphone": "1234567890"
        }

        mocker.patch(
            'app.database.Transactions.find_one',
            side_effect=[None, None]
        )

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data

        use_case = CancelFundUseCase()

        response = use_case.execute(fund_id=1)
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {
            'error_message': 'El usario Test Test no está suscrito al fondo Fund Test'
        }
