from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def assign_user_groups(sender, instance, created, **kwargs):
    if created:
        # Every user is employee
        employees_group, _ = Group.objects.get_or_create(name='Employees')
        instance.groups.add(employees_group)
        
        # Assign manager if needed (optional, we can set manually later)
        # managers_group, _ = Group.objects.get_or_create(name='Managers')
        # if instance.is_staff:  # example condition
        #     instance.groups.add(managers_group)