from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import (Employee, WorkExperience,LanguageTitle, Language,
                     SoftwareSkill, EducationalBackground, JobCategory,
                     State, City, SoftwareSkillCategory, SoftwareSkillTitle,
                     Employer, BasicInformationOfOrganization, JobDetail, FieldOfStudy)
        
 
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
        
    def validate(self, data):
        dependent_cities = City.objects.filter(state=data['state'])
        if data['city'] in dependent_cities:
            return data
        raise serializers.ValidationError(
            'this city does not dependent to selected state')

    

class SoftwareSkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkillCategory
        fields = ['category_title']
        
        
class SoftwareSkillTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkillTitle
        fields = ['title', 'softwareskillcategory']
        

class EmployeeSoftwareSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkill
        fields = ['softwareskillcategory', 'title', 'skill_level']
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return SoftwareSkill.objects.create(employee_id=employee_id,**validated_data)


class EducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = ['degree_level', 'field_of_Study', 'university',
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
        
        
class LanguageTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageTitle
        fields = ['title']
        
        
class JobSeekerLanguageSerializer(serializers.ModelSerializer):
    # languagetitle = LanguageTitleSerializer(many=True)
    class Meta:
        model = Language
        fields = ['languagetitle', 'skill_level']
        
    def create(self, validated_data):
        employee_id = self.context['employee_id']
        return Language.objects.create(employee_id=employee_id,**validated_data)
    
class EmployeeSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(source = "user.first_name", read_only=True)
    last_name = serializers.CharField(source = "user.last_name", read_only=True)
    employee_workexperience = WorkExperienceSerializer(many=True, read_only=True)
    employee_softwareskill = EmployeeSoftwareSkillSerializer(many=True, read_only=True)
    employee_educationalbackground = EducationalBackgroundSerializer(many=True, read_only=True)
    employee_language = JobSeekerLanguageSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = ['user_id','id' ,'first_name','last_name', 'gender',
                  'marital_status', 'phone_number', 'date_of_birth',
                  'expected_salary','Preferred_job_category', 
                  'linkedin_profile', 'state', 'city', 'zip_code',
                  'employee_language','employee_workexperience',
                  'employee_softwareskill','employee_educationalbackground']
        
        
class BasicInformationOfOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInformationOfOrganization
        fields = ['id', 'employer_id', 'name_of_organization',
                  'english_name_of_the_organization', 'website_url', 
                  'industry', 'organization_size', 'state', 
                  'city', 'introduction_of_company', 
                  'companys_field_of_work']
        
    def create(self, validated_data):
        employer_id = self.context['employer_id']
        return BasicInformationOfOrganization.objects.create(employer_id=employer_id,**validated_data)
    

        
class JobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = ['employer_id', 'job_title', 'organizational_category', 'type_of_cooperation', 
                  'priority_with_residents_in_the_city_of_work', 'possibility_of_telecommuting', 
                  'field_of_individual_activity', 'field_of_activity_of_the_organization', 
                  'working_hoursand_days' ,'business_trips_in_this_job', 'minimum_age', 
                  'maximum_age', 'gender', 'attract_an_intern', 'attracting_the_disabled', 
                  'completion_of_military_service', 'the_amount_of_work_experience', 'field_of_Study',
                  'degree_level', 'salary', 'facilities_and_benefits', 'job_description']
        
    def create(self, validated_data):
        employer_id = self.context['employer_pk']
        return JobDetail.objects.create(employer_id=employer_id,**validated_data)
    
    def validate(self, data):
        if data['maximum_age'] > data['minimum_age']:
            return data
        raise serializers.ValidationError(
            'maximum age must be greather than minimum age')

  
class EmployerLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['jobdetail', 'languagetitle', 'skill_level']
        
    def create(self, validated_data):
        employer_id = self.context['employer_pk']
        return Language.objects.create(employer_id=employer_id,**validated_data)


class EmployerSoftwareSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoftwareSkill
        fields = ['jobdetail', 'softwareskillcategory', 'title', 'skill_level']
        
    def create(self, validated_data):
        employer_id = self.context['employer_pk']
        return Language.objects.create(employer_id=employer_id,**validated_data)
 

    
class EmployerSerializer(serializers.ModelSerializer):
    jobdetail_set = JobDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Employer
        fields = ['user_id', 'phone_number', 'organization_level',
                  'direct_corporate_phone_number', 'jobdetail_set']
        
    def create(self, validated_data):
        employer_id = self.context['employer_id']
        return JobDetail.objects.create(employer_id=employer_id,**validated_data)


class JobDetailAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = ['job_title', 'organizational_category', 'type_of_cooperation', 
                  'priority_with_residents_in_the_city_of_work', 'possibility_of_telecommuting', 
                  'field_of_individual_activity', 'field_of_activity_of_the_organization', 
                  'working_hoursand_days' ,'business_trips_in_this_job', 'minimum_age', 
                  'maximum_age', 'gender', 'attract_an_intern', 'attracting_the_disabled', 
                  'completion_of_military_service', 'the_amount_of_work_experience',
                  'field_of_Study', 'degree_level', 'salary', 'facilities_and_benefits',
                  'job_description', 'jobdetail_language']
        

        
class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['title']
        
        