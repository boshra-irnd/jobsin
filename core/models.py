from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
# Create your models here.

class User(AbstractUser):
    ROLE_JOB_SEEKER = 'S'
    ROLE_EMPLOYER = 'E'
    ROLE_CHOICES = [
        (ROLE_JOB_SEEKER, 'Job seeker'),
        (ROLE_EMPLOYER, 'Employer')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)

    
    