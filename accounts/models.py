from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAccount(AbstractUser):
    """
    https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model
    """

    class Meta:
        verbose_name = "User Account"
