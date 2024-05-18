from unittest.mock import patch

import pytest
from rest_framework.test import APITransactionTestCase


class TestCreateOtp(APITransactionTestCase):

    def test_create_otp(self):
        with patch('authorize.views.generate_otp_code') as mock_generate_otp:
            mock_generate_otp.return_value = '123456'

            response = self.client.post(
                data={'phone': '09023145628'},
                path='/otp/',
            )
            assert response.status_code == 201
            assert response.data['otp_code'] is not None
            assert response.data['otp_code'] == '123456'

