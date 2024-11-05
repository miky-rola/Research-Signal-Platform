from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..common import models as base_models
from ..common.validators import email_validator, username_validator


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        if not username:
            username = email.split("@")[0][:15]
        user = self.create_user(
            email, username=username, password=password, **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, base_models.BaseModel):
    email = models.EmailField(
        _("Email address"),
        unique=True,
        validators=[email_validator, MinLengthValidator(8)],
    )
    username = models.CharField(
        _("Username"),
        unique=True,
        blank=True,
        max_length=15,
        validators=[username_validator, MinLengthValidator(4)],
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site"),
    )
    password = models.CharField(
        _("Password"),
        blank=False,
        max_length=128,
        validators=[MinLengthValidator(8)],
    )
    is_verified = models.BooleanField(_("Is Verified"), default=False)
    deleted = models.BooleanField(_("Deleted"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["created_at"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.email


class Profile(base_models.BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_tolerance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    preferred_strategies = models.JSONField(default=list)
    notification_preferences = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.username}'s profile"