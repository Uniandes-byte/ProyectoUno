from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

GENDER=(("F","Female"), ("M","Male"), ("O","Other"))
COUNTRY=(("CO", "Colombia"), ("MX", "México"))

class UserManager(BaseUserManager):
    def create_user(self, email:str, username:str, name:str, password:str = None, is_staff=False, is_superuser=False) -> "User":        
        if not email:
            raise ValueError("User must have an email")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(username=username)
        user.email = self.normalize_email(email)
        user.name = name
        user.set_password(password)
        user.is_active = True 
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_superuser(self, email:str, username:str, name:str, password:str) -> "User":
        user=self.create_user(
            username = username,
            email = email,
            name = name,
            password = password,
            is_staff = True,
            is_superuser = True
        )
        user.save()

class User(AbstractUser):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField("Email", max_length=255, unique=True, blank=False)
    password = models.CharField("Password", max_length=255, null=False)
    name = models.CharField("First Name", max_length=255, null=False)
    
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "username", "name"]
