from django.contrib import admin
from .models import (Employee, WorkExperience, Languages, SoftwareSkills, City, State)
# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'marital_status', 'phone_number', 
                    'date_of_birth', 'expected_salary', 'Preferred_job_category', 
                    'linkedin_profile']
    
    ordering = ['user__first_name', 'user__last_name']
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_id']
    
    
@admin.register(SoftwareSkills)
class SoftwareSkillsAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'level']
@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'skill_level']
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'job_category', 'seniority_level', 'company_name', 'country', 'city', 'from_month', 'from_year', 'to_year', 'to_month', 'current_job', 'achievements_and_main_tasks']
