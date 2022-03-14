from datetime import datetime
from random import choices
from statistics import mode
from django.db import models
from django.test import modify_settings
from languages import fields
from django_countries.fields import CountryField
# Create your models here.

class Employee(models.Model):
    GENDER_FEMALE = 'F'
    GENDER_MALE = 'M'
    GENDER_CHOICES = [
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male')
    ]
    MARITAL_STATUS_SINGLE = 'S'
    MARITAL_STATUS_MARRIED = 'M'
    MARITAL_STATUS_DIVORCED = 'D'
    MARITAL_STATUS_WIDOWED = 'W'
    MARITAL_STATUS = [
        (MARITAL_STATUS_SINGLE, 'Single'),
        (MARITAL_STATUS_MARRIED, 'Married'),
        (MARITAL_STATUS_DIVORCED, 'Divorced'),
        (MARITAL_STATUS_WIDOWED, 'Widowed'), 
    ]

    first_name = models.CharField(max_length=255)	 
    last_name = models.CharField(max_length=255)	
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS)
    # address-id
    phone_number = models.IntegerField(max_length=11)
    date_of_birth = models.DateField()
    expected_salary	= models.IntegerField()
    Preferred_job_category = models.CharField(max_length=255)
    # educational_background-id 
    # work experience-id 
    # languages-id = models.CharField(max_length=255)
    # software skills-id
    linkedin_profile = models.CharField(max_length=255)
    
class Address(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.IntegerField()

class Languages(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    LEVEL_ADVANCED = 'L'
    LEVEL_MEDIUM = 'M'
    LEVEL_INTRODUCTORY = 'I'
    SKILL_LEVEL = [
        (LEVEL_ADVANCED, 'Advanced'),
        (LEVEL_MEDIUM, 'Medium'),
        (LEVEL_INTRODUCTORY, 'Introductory')
    ]
    
    language = fields.LanguageField()
    skill_level = models.CharField(max_length=1, choices=SKILL_LEVEL)

class EducationalBackground(models.Model):
    LEVEL_DIPLOMA = 'DI'
    LEVEL_ASSOCIATE = 'AS'
    LEVEL_BACHELOR = 'BA'
    LEVEL_MASTER = 'MA'
    LEVEL_DOCTORAL = 'DO'
    DEGREE_LEVEL = [
        (LEVEL_DIPLOMA, 'Diploma'),
        (LEVEL_ASSOCIATE, 'Associate'),
        (LEVEL_BACHELOR, 'Bachelor'),
        (LEVEL_MASTER, 'Master'),
        (LEVEL_DOCTORAL, 'Doctoral')
    ]
    
    YEAR_CHOICES = [(y,y) for y in range(1968, datetime.date.today().year)]
    MONTH_CHOICES = [(m,m) for m in range(1,13)]
    
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    degree_level = models.CharField(max_length=2, choices=DEGREE_LEVEL)
    major = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    gpa = models.DecimalField(
        max_digits=6,
        decimal_places=2, 
        null=True)
    from_year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES, 
        null=True, 
        blank=True)
    from_month = models.IntegerField(
        max_length=2,
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    to_year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES,
        null=True, 
        blank=True)
    to_month = models.IntegerField(
        max_length=2,
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    studying =  models.BooleanField()

class SoftwareSkills(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    LEVEL_ADVANCED = 'L'
    LEVEL_MEDIUM = 'M'
    LEVEL_INTRODUCTORY = 'I'
    SKILL_LEVEL = [
        (LEVEL_ADVANCED, 'Advanced'),
        (LEVEL_MEDIUM, 'Medium'),
        (LEVEL_INTRODUCTORY, 'Introductory')
    ]
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=1, choices=SKILL_LEVEL)


class WorkExperience(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_category = models.CharField(max_length=255)
    seniority_level = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    country = CountryField()
    city = models.CharField(max_length=255)
    from_month = models.IntegerField(
        max_length=2,
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    from_year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES, 
        null=True, 
        blank=True)
    to_year = models.IntegerField(
        max_length=4,
        choices=YEAR_CHOICES,
        null=True, 
        blank=True)
    to_month = models.IntegerField(
        max_length=2,
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    current_job = models.BooleanField()
    none = models.BooleanField()
    achievements_and_main_tasks = models.CharField(max_length=1000)