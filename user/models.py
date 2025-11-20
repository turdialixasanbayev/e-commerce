from django.db import models

from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager

from .hashid import encode_id


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser to include additional fields.
    """

    
    first_name = None
    last_name = None
    email = None
    username = None
    # user_permissions = None
    # groups = None
    

    phone_number = PhoneNumberField(
        unique=True,
        db_index=True,
        help_text="User's phone number in international format."
    )

    objects = CustomUserManager()

    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['phone_number']
        indexes = [
            models.Index(fields=["phone_number"]),
        ]

    @property
    def get_hashid(self):
        return encode_id(self.pk)

    def __str__(self):
        return f"{self.pk} {self.phone_number}"
