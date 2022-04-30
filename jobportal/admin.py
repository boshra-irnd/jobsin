from unicodedata import category
from django.contrib import admin
from .models import (JobSeeker, LanguageTitle, WorkExperience,
                     Language, SoftwareSkill, City, State, 
                     SoftwareSkillCategory, SoftwareSkillTitle,
                     Employer, BasicInformationOfOrganization,
                     FieldOfStudy, JobDetail, JobCategory, 
                     Applicant, EducationalBackground)
from django.db.models.aggregates import Count
# Register your models here.


admin.site.site_header = 'Jobsin Admin'
admin.site.index_title = 'Admin'


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'marital_status', 'phone_number', 
                    'date_of_birth', 'expected_salary', 'Preferred_job_category', 
                    'linkedin_profile']
    
    ordering = ['user__first_name', 'user__last_name', 'gender',
                'marital_status', 'date_of_birth', 
                'expected_salary', 'Preferred_job_category',
                'state', 'city']
    list_select_related = ['user']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10
    
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state_name', 'jobseeker_count']
    list_per_page = 10
    list_select_related = ['state']
    list_display_links = ['state_name']

    def state_name(self, city):
        return city.state.name    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(jobseeker_count=Count('jobseeker'))
    
    @admin.display(ordering='jobseeker_count')
    def jobseeker_count(self, city):
        return city.jobseeker_count
    
    
@admin.register(SoftwareSkill)
class SoftwareSkillsAdmin(admin.ModelAdmin):
    list_display = ['jobseeker','jobdetail', 'employer', 
                    'softwareskillcategory', 'title', 'skill_level']
    list_per_page = 10
    
    
@admin.register(SoftwareSkillTitle)
class SoftwareSkillsTitleAdmin(admin.ModelAdmin):
    list_display = ['softwareskillcategory', 'title']
    list_per_page = 10
    
    
@admin.register(LanguageTitle)
class LanguageTitleAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10
  
@admin.register(Language)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['jobseeker','jobdetail', 'employer', 'languagetitle', 'skill_level']
    list_per_page = 10
    
    
@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'job_category', 'seniority_level',
                    'company_name', 'state', 'city', 'from_month',
                    'from_year', 'to_year', 'to_month', 'current_job',
                    'achievements_and_main_tasks']
    list_per_page = 10
    

@admin.register(SoftwareSkillCategory)
class SoftwareSkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_title',]
    list_per_page = 10
    
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'organization_level',
                    'direct_corporate_phone_number']
    list_per_page = 10        
 
 
@admin.register(BasicInformationOfOrganization)
class BasicInformationOfOrganizationAdmin(admin.ModelAdmin):
    list_display = ['employer_id', 'name_of_organization',
                    'english_name_of_the_organization', 'website_url',
                    'organization_phone_number', 'industry', 'organization_size', 
                    'state', 'city', 'introduction_of_company', 'companys_field_of_work']
    list_per_page = 10        
 
 
@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10        


@admin.register(JobDetail)
class JobDetailAdmin(admin.ModelAdmin):
    list_display = ['employer_id', 'job_title', 'organizational_category', 'type_of_cooperation', 
                    'priority_with_residents_in_the_city_of_work', 'possibility_of_telecommuting', 
                    'field_of_individual_activity', 'field_of_activity_of_the_organization', 
                    'working_hoursand_days' ,'business_trips_in_this_job', 'minimum_age', 
                    'maximum_age', 'gender', 'attract_an_intern', 'attracting_the_disabled', 
                    'completion_of_military_service', 'the_amount_of_work_experience', 'field_of_Study',
                    'degree_level', 'salary', 'facilities_and_benefits', 'job_description']
    list_per_page = 10  
    
      
@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10      
    
      
@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['jobseeker', 'cover_letter', 'jobdetail', 'created', 'applicant_status']
    list_per_page = 10        

@admin.register(EducationalBackground)
class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = ['jobseeker', 'degree_level', 'field_of_Study',
                    'university', 'gpa', 'from_year', 'to_year',
                    'from_month', 'to_month', 'studying']