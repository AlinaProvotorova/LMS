from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import UserRole


@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    if sender.name == 'apps.account':
        UserRole.objects.get_or_create(name=UserRole.STUDENT)
        UserRole.objects.get_or_create(name=UserRole.TEACHER)
        UserRole.objects.get_or_create(name=UserRole.MANAGER)
