from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import  Group

User = get_user_model()

@receiver(post_save, sender=User)
def assign_user_groups(sender, instance, created, **kwargs):
    # Ensure Managers and Employee group exists
    managers_group, _ = Group.objects.get_or_create(name="Managers")
    employees_group, _ = Group.objects.get_or_create(name='Employees')
    # Every user is employee
    instance.groups.add(employees_group)
    if instance.is_manager:
        # Add to Managers if user is manager
        instance.groups.add(managers_group)
    else:
        # Remove from Managers if not manager
        instance.groups.remove(managers_group)