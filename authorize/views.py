from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .helpers import generate_otp_code, verification_otp_code
from .models import User
from .serializers import DRFTokenSerializer, OtpSerializer, \
    RegisterUserSerializer, RegisterUserResponseSerializer


class TokenController(TokenObtainPairView):
    serializer_class = DRFTokenSerializer


class OtpGeneratorController(CreateAPIView):
    serializer_class = OtpSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = generate_otp_code(request.data.get('phone'))
        return Response(data=dict(otp_code=otp), status=status.HTTP_201_CREATED)


class UserRegisterController(CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_exists = User.objects.user_exists(
            phone=request.data['phone'],
        )
        if user_exists:
            user = User.objects.filter(phone=request.data['phone']).first()
            data = RegisterUserResponseSerializer(user.first()).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            user = serializer.save()
            data = RegisterUserResponseSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)
