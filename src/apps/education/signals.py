from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import GradingSystem


@receiver(post_migrate)
def create_grades(sender, **kwargs):
    if sender.name == 'apps.education':
        GradingSystem.objects.get_or_create(
            grade=2, grade_ABCDEF='F', grade_in_words='Неудовлетворительно'
        )
        GradingSystem.objects.get_or_create(
            grade=3, grade_ABCDEF='E', grade_in_words='Удовлетворительно'
        )
        GradingSystem.objects.get_or_create(
            grade=4, grade_ABCDEF='D', grade_in_words='Хорошо'
        )
        GradingSystem.objects.get_or_create(
            grade=4, grade_ABCDEF='C', grade_in_words='Очень хорошо'
        )
        GradingSystem.objects.get_or_create(
            grade=5, grade_ABCDEF='В', grade_in_words='Отлично'
        )
        GradingSystem.objects.get_or_create(
            grade=5, grade_ABCDEF='A', grade_in_words='Превосходно'
        )
