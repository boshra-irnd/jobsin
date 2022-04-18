from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_employee_for_new_user(sender, instance, **kwargs):
#     if kwargs['created'] and instance.role == 'E':
#         Employee.objects.create(user=kwargs['instance'])
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_role_for_new_user(sender, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance'] 
        if obj.role == 'S':
            Employee.objects.create(user=kwargs['instance'])