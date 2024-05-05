from django.db import models

# Create your models here.
# accounts/models.py
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, account_id, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, account_id, password, **extra_fields)

    def create_superuser(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, account_id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    account_id = models.CharField(verbose_name=_("account_id"), unique=True, max_length=10)
    email = models.EmailField(verbose_name=_("email"), unique=True)
    password = models.CharField(verbose_name=_("password"), max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    postal_code = models.CharField(verbose_name=_("postal_code"), max_length=12, null=True, blank=True)
    address = models.TextField(verbose_name=_("address"), null=True, blank=True)
    phone_number = models.CharField(verbose_name=_("phone_number"), max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)

    objects = UserManager()

    # accounts/models.py
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['account_id']

    @property
    def username(self):
        return self.account_id

    def __str__(self):
        return self.account_id

