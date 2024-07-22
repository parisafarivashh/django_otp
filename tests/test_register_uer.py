from rest_framework.test import APITransactionTestCase
from unittest.mock import patch


class TestRegister(APITransactionTestCase):

    def test_register(self):
        response = self.client.post(
            data=dict(
                otp_code='1234',
                password='MyPassword',
                phone='09031429689',
            ),
            path='/register/'
        )
        assert response.json() == {'otp_code': ['Otp code is not correct']}

