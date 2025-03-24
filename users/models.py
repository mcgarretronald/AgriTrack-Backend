import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        if not user.id:  # Generate a unique ID if not set
            user.id = self.generate_unique_user_id()

        if password:  # ✅ Ensure password is hashed
            user.set_password(password)  
        else:
            raise ValueError("Password is required")

        user.save(using=self._db)
        return user
    def generate_unique_user_id(self):
        """Generate a unique 16-digit numeric user ID."""
        while True:
            user_id = ''.join(random.choices(string.digits, k=16))  # Generate 16-digit number
            if not User.objects.filter(id=user_id).exists():  
                return user_id

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, max_length=16, unique=True, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username
 
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = User.objects.generate_unique_user_id()  # ✅ Correct
        super().save(*args, **kwargs)
