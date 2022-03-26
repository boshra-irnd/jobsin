from dataclasses import fields
from pyexpat import model
from unicodedata import category
from rest_framework import serializers
from .models import (Employee, WorkExperience,LanguageTitle, Language,
                     SoftwareSkill, EducationalBackground, JobCategory,
                     State, City, SoftwareSkillCategory, SoftwareSkillTitle)
        
class LanguageSerializer(serializers.ModelSerializer):
    languagetitle = serializers.StringRelatedField()
    
    class Meta:
        model = Language
        fields = ['languagetitle', 'skill_level']
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Language.objects.create(employee_id=employee_id,**validated_data)
    
 
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'job_category', 'seniority_level', 
                  'company_name', 'state', 'city', 'from_month', 
                  'from_year', 'to_year', 'to_month', 'current_job', 
                  'achievements_and_main_tasks']
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return WorkExperience.objects.create(employee_id=employee_id,**validated_data)
        

class SoftwareSkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkillCategory
        fields = ['category_title']
        
        
class SoftwareSkillTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkillTitle
        fields = ['title', 'softwareskillcategory']
        

class SoftwareSkillSerializer(serializers.ModelSerializer):
    softwareskillcategory = serializers.StringRelatedField()
    title = serializers.StringRelatedField()
    class Meta:
        model = SoftwareSkill
        fields = ['softwareskillcategory', 'title', 'skill_level']
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return SoftwareSkill.objects.create(employee_id=employee_id,**validated_data)


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = ['degree_level', 'major', 'university',
                  'gpa', 'from_year', 'from_month',
                  'to_year', 'to_month', 'studying']
    
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return EducationalBackground.objects.create(employee_id=employee_id,**validated_data)
    
        
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['title']
        
class StateSerializer(serializers.Serializer):
    class Meta:
        models = State
        fields = ['title']
class CitySerializer(serializers.Serializer):
    class Meta:
        models = City
        fields = ['title']   
        
class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(source = "user.first_name", read_only=True)
    last_name = serializers.CharField(source = "user.last_name", read_only=True)
    employee_workexperience = WorkExperienceSerializer(many=True, read_only=True)
    employee_softwareskill = SoftwareSkillSerializer(many=True, read_only=True)
    employee_educationalbackground = EducationalBackgroundSerializer(many=True, read_only=True)
    employee_language = LanguageSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ['user_id','id' ,'first_name','last_name', 'gender',
                  'marital_status', 'phone_number', 'date_of_birth',
                  'expected_salary','Preferred_job_category', 
                  'linkedin_profile', 'state', 'city', 'zip_code',
                  'employee_language','employee_workexperience',
                  'employee_softwareskill','employee_educationalbackground']
        
class LanguageTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageTitle
        fields = ['title']