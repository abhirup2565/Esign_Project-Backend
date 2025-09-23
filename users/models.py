from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    # Use is_staff as manager flag

    def __str__(self):
        return self.username