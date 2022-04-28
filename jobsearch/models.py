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
from django.db.models import Q
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
    field_of_Study = models.ForeignKey('FieldOfStudy', on_delete=models.CASCADE)
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
        ordering = ['degree_level', 'field_of_Study', 'university', 'gpa']
        index_together = [
            ['from_year', 'to_year'],
            ['from_month', 'to_month']
            ]

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
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_softwareskill', null=True, blank=True)
    jobdetail = models.ForeignKey('JobDetail',on_delete=models.PROTECT, related_name='jobdetail_softwareskill', null=True, blank=True)
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
        index_together = [
            ['from_year', 'to_year'],
            ['from_month', 'to_month']
            ]



# -----------------------------------------------------------
# karfarma


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)	
    phone_number = models.CharField(max_length=11)
    organization_level = models.CharField(max_length=55)
    direct_corporate_phone_number = models.CharField(max_length=10)
    
class BasicInformationOfOrganization(models.Model):
    employer = models.OneToOneField(Employer, on_delete=models.PROTECT)
    name_of_organization = models.CharField(max_length=255)
    english_name_of_the_organization = models.CharField(max_length=255)
    website_url = models.CharField(max_length=255)
    organization_phone_number = models.CharField(max_length=20)
    industry = models.CharField(max_length=255)
    organization_size = models.PositiveIntegerField()
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    introduction_of_company = models.CharField(max_length=255)
    companys_field_of_work = models.CharField(max_length=255)


class FieldOfStudy(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return (self.title)
    

class JobDetail(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.PROTECT)
    job_title = models.CharField(max_length=255)
    organizational_category = models.CharField(max_length=255)
    type_of_cooperation = models.CharField(max_length=255)
    priority_with_residents_in_the_city_of_work = models.BooleanField()
    possibility_of_telecommuting = models.BooleanField()
    field_of_individual_activity = models.CharField(max_length=255)
    field_of_activity_of_the_organization = models.CharField(max_length=255)
    working_hoursand_days = models.CharField(max_length=255, help_text='8-12 all day of week')
    business_trips_in_this_job = models.BooleanField(max_length=255, blank=True, null=True)
    
    AGE_CHOICES = [(m,m) for m in range(18,50)]
    minimum_age = models.CharField(max_length=2, choices=AGE_CHOICES)
    maximum_age = models.CharField(max_length=2, choices=AGE_CHOICES)
    
    GENDER_NONE = 'N'
    GENDER_FEMALE = 'F'
    GENDER_MALE = 'M'
    GENDER_CHOICES = [
        (GENDER_NONE, 'Does not matter'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    
    attract_an_intern = models.BooleanField()
    attracting_the_disabled = models.BooleanField()
    completion_of_military_service = models.BooleanField()
    WORK_EXPERIENCE_CHOICES = [(m,m) for m in range(0,18)]
    the_amount_of_work_experience = models.CharField(max_length=2, choices=WORK_EXPERIENCE_CHOICES)
    field_of_Study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE,null=True ,blank=True)
    
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
    
    degree_level = models.CharField(max_length=2, choices=DEGREE_LEVEL)
    # software_skills-id
    # language_id
    
    SALARY_1 = '2-3'
    SALARY_2 = '3-4'
    SALARY_3 = '4-5'
    SALARY_4 = '5-6'
    SALARY_5 = '6-8'
    SALARY_6 = '8-10'
    SALARY_7 = '10-12'
    SALARY_8 = '12-16'
    SALARY_9 = '16-20'
    SALARY_10 = '20-25'
    SALARY_11 = '25 - ?'

    SALARY_CHOICES = [
        (SALARY_1, '2 to 3 million tomans'),
        (SALARY_2, '3 to 4 million tomans'),
        (SALARY_3, '4 to 5 million tomans'),
        (SALARY_4, '5 to 6 million tomans'),
        (SALARY_5, '6 to 8 million tomans'),
        (SALARY_6, '8 to 10 million tomans'),
        (SALARY_7, '10 to 12 million tomans'),
        (SALARY_8, '12 to 16 million tomans'),
        (SALARY_9, '16 to 20 million tomans'),
        (SALARY_10, '20 to 25 million tomans'),
        (SALARY_11, '25 million tomans and above'),
    ]

    salary = models.CharField(max_length=6, choices=SALARY_CHOICES)
    facilities_and_benefits = models.CharField(max_length=255, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)
    def __str__(self):
        return (self.job_title) + ' | ' + (self.job_description[0:10])
    
        



    
class Language(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_language', null=True, blank=True)
    jobdetail = models.ForeignKey(JobDetail,on_delete=models.PROTECT, related_name='jobdetail_language', null=True, blank=True)
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
        constraints = [
            models.CheckConstraint(
                check=Q(employee__isnull=False) | Q(jobdetail__isnull=False),
                name='not_both_null'
            )
        ]
