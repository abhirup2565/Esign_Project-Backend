from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # change reverse accessor
        blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # change reverse accessor
        blank=True,
        help_text='Specific permissions for this user.'
    )