from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

User = settings.AUTH_USER_MODEL  # Use custom user

from django.apps import apps
User = apps.get_model(settings.AUTH_USER_MODEL)

@receiver(post_save, sender=User)
def assign_user_groups(sender, instance, created, **kwargs):
    # Ensure groups exist
    managers_group, _ = Group.objects.get_or_create(name="Managers")
    employees_group, _ = Group.objects.get_or_create(name='Employees')

    if created:
        # Every user is employee
        instance.groups.add(employees_group)
        # If user is manager, also add to Managers
        if getattr(instance, "is_manager", False):
            instance.groups.add(managers_group)
    else:
        # Update groups if existing user is changed
        if getattr(instance, "is_manager", False):
            instance.groups.add(managers_group)
        else:
            instance.groups.remove(managers_group)