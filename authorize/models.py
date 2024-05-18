from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, phone, password):
        user = self.model(phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    phone_regex = RegexValidator(
        regex=r'09(\d{9})$',
        message="Enter a valid phone_number"
    )
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=15, validators=[phone_regex], unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_system = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['']

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'user'
        ordering = ['id']

