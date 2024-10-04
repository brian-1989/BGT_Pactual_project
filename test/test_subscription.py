from app.use_cases.subscription import SubscriptionFundUseCase
from fastapi import status
import json

class TestForFundSubscription():

    def test_successful_subscription_with_email(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')
        mock_transactions = mocker.patch('app.database.Transactions.find_one')
        mock_serializer = mocker.patch('app.serializer.serializerTransaction')
        mock_send_email = mocker.patch.object(SubscriptionFundUseCase, 'send_to_email')

        mocker.patch('app.database.Users.find_one_and_update')
        mocker.patch('app.database.Transactions.insert_one')

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
            "fund_name": "Fund Test",
            "transaction_type": "subscription",
            "amount": 100,
            "status": "active",
            "created_at": "2023-10-01"
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data
        mock_transactions.return_value = None
        mock_serializer.return_value = transaction_data

        use_case = SubscriptionFundUseCase()

        # Act
        response = use_case.execute(fund_id=1, notification_type="email")
        response_json  = json.loads(response.body.decode("utf-8"))

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response_json == {
            "success_message": "La suscripción al fondo Fund Test fue completada. El nuevo monto es de 100"
        }
        mock_send_email.assert_called_once_with(receiver_email="test@test.com", fund_name="Fund Test")

    def test_successful_subscription_with_sms(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')
        mock_transactions = mocker.patch('app.database.Transactions.find_one')
        mock_serializer = mocker.patch('app.serializer.serializerTransaction')
        mock_send_sms = mocker.patch.object(SubscriptionFundUseCase, 'send_to_sms')

        mocker.patch('app.database.Users.find_one_and_update')
        mocker.patch('app.database.Transactions.insert_one')

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
            "fund_name": "Fund Test",
            "transaction_type": "subscription",
            "amount": 100,
            "status": "active",
            "created_at": "2023-10-01"
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data
        mock_transactions.return_value = None
        mock_serializer.return_value = transaction_data

        use_case = SubscriptionFundUseCase()

        # Act
        response = use_case.execute(fund_id=1, notification_type="sms")
        response_json  = json.loads(response.body.decode("utf-8"))

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response_json == {
            "success_message": "La suscripción al fondo Fund Test fue completada. El nuevo monto es de 100"
        }
        mock_send_sms.assert_called_once_with(cellphone="1234567890", fund_name="Fund Test")

    def test_failed_subscription_by_not_fund(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_funds.return_value = None

        use_case = SubscriptionFundUseCase()

        response = use_case.execute(fund_id=1, notification_type="email")
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {'error_message': 'El fondo no fue encontrado'}
    
    def test_failed_subscription_by_not_user(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')

        fund_data = {
            "_id": 1,
            "name": "Fund Test",
            "minimum_amount": 100
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = None

        use_case = SubscriptionFundUseCase()

        response = use_case.execute(fund_id=1, notification_type="email")
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {'error_message': 'El usuario no fue encontrado'}

    def test_failed_subscription_by_subscribed_to_the_fund(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')
        mock_transactions = mocker.patch('app.database.Transactions.find_one')

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
            "fund_name": "Fund Test",
            "transaction_type": "subscription",
            "amount": 100,
            "status": "active",
            "created_at": "2023-10-01"
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data
        mock_transactions.return_value = transaction_data

        use_case = SubscriptionFundUseCase()

        response = use_case.execute(fund_id=1, notification_type="email")
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {
            'error_message': 'El usario Test Test ya se enceuntra suscrito al fondo Fund Test'
        }

    def test_failed_subscription_by_not_amount(self, mocker):
        mock_funds = mocker.patch('app.database.Funds.find_one')
        mock_users = mocker.patch('app.database.Users.find_one')
        mock_transactions = mocker.patch('app.database.Transactions.find_one')
        mock_serializer = mocker.patch('app.serializer.serializerTransaction')

        fund_data = {
            "_id": 1,
            "name": "Fund Test",
            "minimum_amount": 100
        }
        user_data = {
            "_id": "1",
            "name": "Test Test",
            "balance": 50,
            "email": "test@test.com",
            "cellphone": "1234567890"
        }
        transaction_data = {
            "transaction_id": "123",
            "fund_id": "1",
            "fund_name": "Fund Test",
            "transaction_type": "subscription",
            "amount": 100,
            "status": "active",
            "created_at": "2023-10-01"
        }

        mock_funds.return_value = fund_data
        mock_users.return_value = user_data
        mock_transactions.return_value = None
        mock_serializer.return_value = transaction_data

        use_case = SubscriptionFundUseCase()

        response = use_case.execute(fund_id=1, notification_type="email")
        response_json  = json.loads(response.body.decode("utf-8"))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == {'error_message': 'No tiene saldo disponible para vincularse al fondo Fund Test'}
