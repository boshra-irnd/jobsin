from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobSeeker, Employer
      

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_role_for_new_user(sender, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance'] 
        if obj.role == 'S':
            JobSeeker.objects.create(user=kwargs['instance'])
        else:
            Employer.objects.create(user=kwargs['instance'])