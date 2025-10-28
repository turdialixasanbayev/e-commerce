import re

from django.contrib.auth.models import UserManager

from django.core.exceptions import ValidationError



class CustomUserManager(UserManager):
    """
    Custom phone number auth manager.
    """

    def validate_phone(self, phone_number):
        phone_number_str = str(phone_number)
        pattern = r"^\+?\d{9,15}$"
        if not re.match(pattern, phone_number_str):
            raise ValidationError("Invalid phone number format!")
        return phone_number

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number field is required.")
        
        self.validate_phone(phone_number)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(phone_number=phone_number, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user ### use Python
    
    """
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)

        use Django
    """
