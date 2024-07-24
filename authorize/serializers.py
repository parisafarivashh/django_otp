from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from authorize.helpers import verification_otp_code
from authorize.models import User


class DRFTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token['phone'] = user.phone
        return token


class RegisterUserSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'otp_code']

    def validate(self, attrs):
        otp_provided = attrs.pop('otp_code')
        phone = attrs.get('phone')
        if not verification_otp_code(phone, otp_provided):
            error = {"otp_code": ["Otp code is not correct"]}
            raise ValidationError(detail=error)
        return super().validate(attrs)

    def create(self, validated_data):
        user_exists = User.objects.user_exists(
            phone=validated_data['phone'],
        )
        if user_exists:
            return User.objects.filter(phone=validated_data['phone']).first()

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_verified = True
        user.save()
        # user = User.objects.create_user(
        #     phone=validated_data['phone'],
        #     password=validated_data['password']
        # )
        return user


class RegisterUserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class OtpSerializer(serializers.Serializer):
    phone_regex = RegexValidator(
        regex=r'09(\d{9})$',
        message="Enter a valid phone_number"
    )
    phone = serializers.CharField(validators=[phone_regex])


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_admin = True
        user.save()
        return user


