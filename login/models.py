from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullaname, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullaname=fullaname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullaname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, fullaname, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    fullaname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    meta_id = models.CharField(max_length=255, blank=True, null=True)
    meta_token = models.CharField(max_length=255, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    google_token = models.CharField(max_length=255, blank=True, null=True)
    twitter_id = models.CharField(max_length=255, blank=True, null=True)
    twitter_token = models.CharField(max_length=255, blank=True, null=True)
    img_url = models.URLField(blank=True, null=True)
    auth_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullaname']

    def __str__(self):
        return self.fullaname

class EmailUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    verify_code = models.CharField(max_length=6, blank=True, null=True)
    login_token = models.CharField(max_length=100, blank=True, null=True)
    date_last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email