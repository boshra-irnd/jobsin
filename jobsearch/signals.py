from turtle import pos
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_employee_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Employee.objects.create(user=kwargs['instance'])