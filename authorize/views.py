from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .authentication import AdminTokenAuthentication
from .helpers import generate_otp_code
from .models import User
from .serializers import DRFTokenSerializer, OtpSerializer, \
    RegisterUserSerializer, RegisterUserResponseSerializer, AdminUserSerializer


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
        user = serializer.save()
        data = RegisterUserResponseSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)


class AdminLoginController(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data['phone']
        password = request.data['password']
        user = authenticate(username=phone, password=password)
        if user and user.is_admin:
            token = Token.object.get_or_create(user=user)
            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials or not an admin'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAdminController(generics.CreateAPIView):
    authentication_classes = [AdminTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

