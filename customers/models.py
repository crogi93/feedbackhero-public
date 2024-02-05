from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from customers.managers import *
from core.models import TimestampMixin

from datetime import datetime


class User(AbstractBaseUser, TimestampMixin):
    email = models.EmailField(_("email adress"), unique=True)
    email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    terms_accepted = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def is_deleted(self) -> bool:
        return self.deleted_at

    def set_deleted(self) -> None:
        self.deleted_at = datetime.now()

    def is_confirmed(self) -> bool:
        self.email_verified
