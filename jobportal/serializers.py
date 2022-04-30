from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import (JobSeeker, WorkExperience,LanguageTitle, Language,
                     SoftwareSkill, EducationalBackground, JobCategory,
                     State, City, SoftwareSkillCategory, SoftwareSkillTitle,
                     Employer, BasicInformationOfOrganization, JobDetail,
                     FieldOfStudy, Applicant)
        
 
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'job_category', 'seniority_level', 
                  'company_name', 'state', 'city', 'from_month', 
                  'from_year', 'to_year', 'to_month', 'current_job', 
                  'achievements_and_main_tasks']
        
    def create(self, validated_data):
        jobseeker_id = self.context['jobseeker_id']
        return WorkExperience.objects.create(jobseeker_id=jobseeker_id,**validated_data)
        
    def validate(self, data):
        dependent_cities = City.objects.filter(state=data['state'])
        if data['city'] not in dependent_cities:
            raise serializers.ValidationError(
                'this city does not dependent to selected state')
        if data['from_year'] > data['to_year']:
            raise serializers.ValidationError(
            {"to_year": "finish must occur after start"})
        elif data['from_year'] == data['to_year']:
            if data['from_month'] >= data['to_month']:
                raise serializers.ValidationError(
                    {"to_month": "finish must occur after start"})
        return data
        
      

    

    

class SoftwareSkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkillCategory
        fields = ['category_title']
        
        
class SoftwareSkillTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkillTitle
        fields = ['title', 'softwareskillcategory']
        

class JobSeekerSoftwareSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSkill
        fields = ['softwareskillcategory', 'title', 'skill_level']
        
    def create(self, validated_data):
        jobseeker_id = self.context['jobseeker_id']
        return SoftwareSkill.objects.create(jobseeker_id=jobseeker_id,**validated_data)

    def create(self, validated_data):
        employer_id = self.context['employer_id']
        return SoftwareSkill.objects.create(employer_id=employer_id,**validated_data)
 
 
class EducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = ['degree_level', 'field_of_Study', 'university',
                  'gpa', 'from_year', 'from_month',
                  'to_year', 'to_month', 'studying']
    
    def create(self, validated_data):
        jobseeker_id = self.context['jobseeker_id']
        return EducationalBackground.objects.create(jobseeker_id=jobseeker_id,**validated_data)
    
    def validate(self, data):
        if data['from_year'] > data['to_year']:
            raise serializers.ValidationError(
            {"to_year": "finish must occur after start"})
        elif data['from_year'] == data['to_year']:
            if data['from_month'] >= data['to_month']:
                raise serializers.ValidationError(
                    {"to_month": "finish must occur after start"})
        return data
    
        
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
        jobseeker_id = self.context['jobseeker_id']
        return Language.objects.create(jobseeker_id=jobseeker_id,**validated_data)
    
class JobSeekerSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    first_name = serializers.CharField(source = "user.first_name", read_only=True)
    last_name = serializers.CharField(source = "user.last_name", read_only=True)
    jobseeker_workexperience = WorkExperienceSerializer(many=True, read_only=True)
    jobseeker_softwareskill = JobSeekerSoftwareSkillSerializer(many=True, read_only=True)
    jobseeker_educationalbackground = EducationalBackgroundSerializer(many=True, read_only=True)
    jobseeker_language = JobSeekerLanguageSerializer(many=True, read_only=True)
    class Meta:
        model = JobSeeker
        fields = ['user_id','id' ,'first_name','last_name', 'gender',
                  'marital_status', 'phone_number', 'date_of_birth',
                  'expected_salary','Preferred_job_category', 
                  'linkedin_profile', 'state', 'city', 'zip_code',
                  'jobseeker_language','jobseeker_workexperience',
                  'jobseeker_softwareskill','jobseeker_educationalbackground']
        
    
    def validate(self, data):
        dependent_cities = City.objects.filter(state=data['state'])
        if data['city'] not in dependent_cities:
            raise serializers.ValidationError(
                'this city does not dependent to selected state')
        return data
    
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
    
    def validate(self, data):
        dependent_cities = City.objects.filter(state=data['state'])
        if data['city'] not in dependent_cities:
            raise serializers.ValidationError(
                'this city does not dependent to selected state')
        return data
  
class EmployerLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ['jobdetail', 'languagetitle', 'skill_level']
        
    def create(self, validated_data):
        employer_id = self.context['employer_id']
        return Language.objects.create(employer_id=employer_id,**validated_data)


class EmployerSoftwareSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoftwareSkill
        fields = ['jobdetail', 'softwareskillcategory', 'title', 'skill_level']
        
    def create(self, validated_data):
        employer_id = self.context['employer_id']
        return SoftwareSkill.objects.create(employer_id=employer_id,**validated_data)
 
    def validate(self, data):
        dependent_skills = SoftwareSkillTitle.objects.filter(softwareskillcategory=data['softwareskillcategory'])
        if data['title'] not in dependent_skills :
            raise serializers.ValidationError(
                {'title':f'{data["title"]} does not dependent to {data["softwareskillcategory"]}'})
        return data
    
class JobDetailSerializer(serializers.ModelSerializer):
    jobdetail_language = EmployerLanguageSerializer(read_only=True, many=True)
    jobdetail_softwareskill = EmployerSoftwareSkillSerializer(read_only=True, many=True)
    class Meta:
        model = JobDetail
        fields = ['employer_id', 'job_title', 'organizational_category', 'type_of_cooperation', 
                  'priority_with_residents_in_the_city_of_work', 'possibility_of_telecommuting', 
                  'field_of_individual_activity', 'field_of_activity_of_the_organization', 
                  'working_hoursand_days' ,'business_trips_in_this_job', 'minimum_age', 
                  'maximum_age', 'gender', 'attract_an_intern', 'attracting_the_disabled', 
                  'completion_of_military_service', 'the_amount_of_work_experience',
                  'field_of_Study', 'degree_level', 'salary', 'facilities_and_benefits',
                  'job_description', 'jobdetail_language', 'jobdetail_softwareskill']
        
    def create(self, validated_data):
        employer_id = self.context['employer_pk']
        return JobDetail.objects.create(employer_id=employer_id,**validated_data)
    
    def validate(self, data):
        if data['maximum_age'] > data['minimum_age']:
            return data
        raise serializers.ValidationError(
            'maximum age must be greather than minimum age')


    
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
    jobdetail_language = EmployerLanguageSerializer(read_only=True, many=True)
    jobdetail_softwareskill = EmployerSoftwareSkillSerializer(read_only=True, many=True)
    class Meta:
        model = JobDetail
        fields = ['job_title', 'organizational_category', 'type_of_cooperation', 
                  'priority_with_residents_in_the_city_of_work', 'possibility_of_telecommuting', 
                  'field_of_individual_activity', 'field_of_activity_of_the_organization', 
                  'working_hoursand_days' ,'business_trips_in_this_job', 'minimum_age', 
                  'maximum_age', 'gender', 'attract_an_intern', 'attracting_the_disabled', 
                  'completion_of_military_service', 'the_amount_of_work_experience',
                  'field_of_Study', 'degree_level', 'salary', 'facilities_and_benefits',
                  'job_description', 'jobdetail_language', 'jobdetail_softwareskill']
        

        
class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['title']
        
class JobSeekerApplicantSerializer(serializers.ModelSerializer):
    applicant_status = serializers.CharField(read_only=True)
    class Meta:
        model = Applicant
        fields = ['cover_letter', 'jobdetail', 'created', 'applicant_status']
        
    def create(self, validated_data):
        jobseeker_id = self.context['jobseeker_id']
        return Applicant.objects.create(jobseeker_id=jobseeker_id,**validated_data)

class EmployerApplicantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    jobdetail = JobDetailSerializer(read_only=True)
    jobseeker = JobSeekerSerializer(read_only=True)
    cover_letter = serializers.CharField(read_only=True)
    class Meta:
        model = Applicant
        fields = ['id', 'jobseeker', 'cover_letter', 'jobdetail', 'created', 'applicant_status']
        
 
class EmployerEducationalBackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalBackground
        fields = ['jobdetail', 'degree_level', 'field_of_Study', 'university',
                  'gpa', 'from_year', 'from_month',
                  'to_year', 'to_month', 'studying']
    
    def create(self, validated_data):
        jobdetail_id = self.context['jobdetail_id']
        return EducationalBackground.objects.create(jobdetail_id=jobdetail_id,**validated_data)
    
    def validate(self, data):
        if data['from_year'] > data['to_year']:
            raise serializers.ValidationError(
            {"to_year": "finish must occur after start"})
        elif data['from_year'] == data['to_year']:
            if data['from_month'] >= data['to_month']:
                raise serializers.ValidationError(
                    {"to_month": "finish must occur after start"})
        return data
    