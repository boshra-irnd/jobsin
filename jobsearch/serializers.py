from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import (Employee, Address, WorkExperience, Languages, SoftwareSkills, EducationalBackground, JobCategory)


class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Address.objects.create(employee_id=employee_id,**validated_data)
    
    class Meta:
        model = Address
        fields = ['state', 'city', 'zip_code']
        
        
class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ['language', 'skill_level']
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Employee
        fields = ['user_id','id' ,'first_name','last_name', 'gender', 'marital_status', 
                  'phone_number', 'date_of_birth', 'expected_salary',
                  'Preferred_job_category', 'linkedin_profile', 
                  'employee_arrdess', 'employee_language',
                  'employee_workexperience', 'employee_softwareskill',
                  'employee_educationalbackground']
    employee_language = LanguagesSerializer(many=True, read_only=True)

        
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'job_category', 'seniority_level', 
                  'company_name', 'country', 'city', 'from_month', 
                  'from_year', 'to_year', 'to_month', 'current_job', 
                  'none', 'achievements_and_main_tasks']
class SoftwareSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkills
        fields = ['category', 'title', 'level']

class EducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = ['degree_level', 'major', 'university',
                  'gpa', 'from_year', 'from_month',
                  'to_year', 'to_month', 'studying']
        
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['title']