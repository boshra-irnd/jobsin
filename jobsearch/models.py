from datetime import datetime
from pyexpat import model
from random import choices
from re import L
from statistics import mode
from turtle import title
from django.db import models
from django.test import modify_settings
from django.conf import settings
from django.contrib import admin

# Create your models here.


class JobCategory(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title
       
       
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)	
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS)
    # address-id
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    expected_salary	= models.IntegerField(null=True, blank=True)
    Preferred_job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    # work experience-id 
    # languages-id = models.CharField(max_length=255)
    # software skills-id
    linkedin_profile = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    # class Meta:
    #     ordering = ['gender', 'marital_status', 'date_of_birth', 
    #                 'expected_salary', 'Preferred_job_category',
    #                 'state', 'city']

    
class State(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta: #show the plural of city as cities instead of citys
        verbose_name_plural = 'cities'
        ordering = ['name']
        
        
class LanguageTitle(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.title
    
class Language(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_language')

    LEVEL_ADVANCED = 'A'
    LEVEL_MEDIUM = 'M'
    LEVEL_INTRODUCTORY = 'I'
    SKILL_LEVEL = [
        (LEVEL_ADVANCED, 'Advanced'),
        (LEVEL_MEDIUM, 'Medium'),
        (LEVEL_INTRODUCTORY, 'Introductory')
    ]
    
    languagetitle = models.ForeignKey(LanguageTitle, on_delete=models.PROTECT)
    skill_level = models.CharField(max_length=1, choices=SKILL_LEVEL)
    
    def __str__(self) -> str:
        return (f'{self.languagetitle} | {self.skill_level}')
    
    class Meta:
        ordering = ['languagetitle', 'skill_level']

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
    
    YEAR_CHOICES = [(y,y) for y in range(1968, datetime.now().year)]
    MONTH_CHOICES = [(m,m) for m in range(1,13)]
    
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_educationalbackground')
    degree_level = models.CharField(max_length=2, choices=DEGREE_LEVEL)
    major = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    gpa = models.DecimalField(
        max_digits=6,
        decimal_places=2, 
        null=True)
    from_year = models.IntegerField(
        choices=YEAR_CHOICES, 
        null=True, 
        blank=True)
    from_month = models.IntegerField(
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    to_year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=True, 
        blank=True)
    to_month = models.IntegerField(
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    studying =  models.BooleanField()

    class Meta:
        ordering = ['degree_level', 'major', 'university', 'gpa']


class SoftwareSkillCategory(models.Model):
    category_title = models.CharField(max_length=255,)
    
    def __str__(self) -> str:
        return (self.category_title)
    
    class Meta:
        ordering = ['id']

    
class SoftwareSkillTitle(models.Model):
    title = models.CharField(max_length=255)
    softwareskillcategory = models.ForeignKey(SoftwareSkillCategory, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['id']


class SoftwareSkill(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_softwareskill')
    
    LEVEL_ADVANCED = 'L'
    LEVEL_MEDIUM = 'M'
    LEVEL_INTRODUCTORY = 'I'
    
    SKILL_LEVEL = [
        (LEVEL_ADVANCED, 'Advanced'),
        (LEVEL_MEDIUM, 'Medium'),
        (LEVEL_INTRODUCTORY, 'Introductory')
    ]
    
    softwareskillcategory = models.ForeignKey(SoftwareSkillCategory, on_delete=models.PROTECT)
    title = models.ForeignKey(SoftwareSkillTitle, on_delete=models.PROTECT)
    skill_level = models.CharField(max_length=1, choices=SKILL_LEVEL)

    class Meta:
        ordering = ['title', 'skill_level', 'softwareskillcategory']


class WorkExperience(models.Model):
    YEAR_CHOICES = [(y,y) for y in range(1968, datetime.now().year)]
    MONTH_CHOICES = [(m,m) for m in range(1,13)]
    
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_workexperience')
    job_title = models.CharField(max_length=255)
    job_category = models.CharField(max_length=255)
    seniority_level = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    from_month = models.IntegerField(
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    from_year = models.IntegerField(
        choices=YEAR_CHOICES, 
        null=True, 
        blank=True)
    to_year = models.IntegerField(
        choices=YEAR_CHOICES,
        null=True, 
        blank=True)
    to_month = models.IntegerField(
        choices=MONTH_CHOICES,
        null=True, 
        blank=True)
    current_job = models.BooleanField()
    achievements_and_main_tasks = models.TextField(max_length=1000)
    
    class Meta:
        ordering = ['job_title', 'job_category', 'seniority_level',
                    'company_name', 'state', 'city', 'current_job']


