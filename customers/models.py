import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.basemodels import TimestampMixin
from customers.managers import *


class PasswordValidator:
    @staticmethod
    def validate(password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(settings.PASSWORD_REGEX, password):
            raise ValidationError(
                "Password must contain at least one upper case letter, one lower case letter, and one number."
            )

    @staticmethod
    def get_help_text():
        return "Your password must be at least 8 characters long and contain at least one upper case letter, one lower case letter, and one number."


class User(AbstractBaseUser, TimestampMixin):
    email = models.EmailField(_("email adress"), unique=True)
    email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    terms_accepted = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    password_validator = PasswordValidator()

    password = models.CharField(
        _("password"),
        max_length=128,
        validators=[password_validator.validate],
        help_text=password_validator.get_help_text,
    )

    def __str__(self) -> str:
        return self.email

    def is_deleted(self) -> bool:
        return self.deleted_at

    def set_deleted(self) -> None:
        self.deleted_at = datetime.now()

    def is_confirmed(self) -> bool:
        self.email_verified
