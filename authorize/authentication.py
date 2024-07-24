from typing import Optional, Tuple

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.tokens import Token


class CustomJwtAuthentication(JWTAuthentication):

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is not None:
            user, _ = user_auth_tuple
            if user.is_admin is True:
                raise AuthenticationFailed(_("This token is not valid"), code="valid_token")
        return user_auth_tuple
    
    
class AdminTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        tuple_user = super().authenticate_credentials(key)
        if tuple_user is not None:
            user, _ = tuple_user
            if user.is_admin is False:
                raise AuthenticationFailed(_("This token is not valid"), code="valid_token")

        return tuple_user





