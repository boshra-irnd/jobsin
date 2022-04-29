from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins, generics
from rest_framework import status
from rest_framework.permissions import (AllowAny, DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly,
                                        IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import (IsAdminOrReadOnly, IsOwnUserOrReadOnly, 
                          IsOwnUserOrReadOnlyEmployer, IsOwnUserOrReadOnlyEmployer2)
from .pagination import DefaultPagination
from .serializers import (JobSeekerSerializer, JobSeekerSoftwareSkillSerializer,
                          JobSeekerLanguageSerializer, EducationalBackgroundSerializer, StateSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer,
                          LanguageTitleSerializer, SoftwareSkillCategorySerializer,
                          SoftwareSkillTitleSerializer, EmployerSerializer, 
                          BasicInformationOfOrganizationSerializer, FieldOfStudySerializer, 
                          JobDetailSerializer, EmployerLanguageSerializer, JobSeekerApplicantSerializer,
                          JobDetailAllUserSerializer, EmployerSoftwareSkillSerializer, EmployerApplicantSerializer)
from .models import (JobSeeker, Language, SoftwareSkill,WorkExperience,
                     JobCategory, EducationalBackground, LanguageTitle, 
                     SoftwareSkillTitle, SoftwareSkillCategory, Employer, 
                     BasicInformationOfOrganization, FieldOfStudy,
                     JobDetail, Applicant)


class JobSeekerViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    lookup_url_kwarg = "id"
    permission_classes = [IsOwnUserOrReadOnly,IsAuthenticated]
    pagination_class = DefaultPagination
    serializer_class = JobSeekerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['date_of_birth']
    # search_fields = ['jobseeker_educationalbackground__university']
    # filterset_fields = ['Preferred_job_category', 
    #                     'jobseeker_educationalbackground__degree_level',
    #                     'gender', 'state', 'city']
    
    
    def get_queryset(self):
        return JobSeeker.objects \
        .select_related('user', 'Preferred_job_category', 'state', 'city') \
        .filter(user_id=self.request.user.id)

class JobSeekerSoftwareSkillViewSet(ModelViewSet):
    serializer_class = JobSeekerSoftwareSkillSerializer

    def dispatch(self, request, *args, **kwargs):
        parent_view = JobSeekerViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["jobseeker_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        return SoftwareSkill.objects \
            .filter(jobseeker__user_id=self.request.user.jobseeker.id) \
            .order_by('id').select_related('jobseeker','softwareskillcategory','title')
    
    def get_serializer_context(self):
        return {'jobseeker_id': self.request.user.jobseeker.id}


class JobSeekerLanguageViewSet(ModelViewSet):
    serializer_class = JobSeekerLanguageSerializer
    
    
    def dispatch(self, request, *args, **kwargs):
        parent_view = JobSeekerViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["jobseeker_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)

    
    def get_queryset(self):
        return Language.objects.select_related('languagetitle','jobseeker') \
            .filter(jobseeker__user_id=self.request.user.jobseeker.id)

    def get_serializer_context(self):
        return {'jobseeker_id': self.kwargs['jobseeker_id']}
 
    
class WorkExperienceViewSet(ModelViewSet):
    serializer_class = WorkExperienceSerializer
    
    def dispatch(self, request, *args, **kwargs):
        parent_view = JobSeekerViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["jobseeker_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)

    
    def get_queryset(self):
        return WorkExperience.objects \
            .filter(jobseeker__user_id=self.request.user.jobseeker.id) \
            .select_related('state')
    
    def get_serializer_context(self):
        return {'jobseeker_id': self.kwargs['jobseeker_id']}



class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    

class EducationalBackgroundViewSet(ModelViewSet):
    serializer_class = EducationalBackgroundSerializer
    
    def dispatch(self, request, *args, **kwargs):
        parent_view = JobSeekerViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["jobseeker_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return EducationalBackground.objects \
            .filter(jobseeker__user_id=self.request.user.jobseeker.id)
    
    def get_serializer_context(self):
        return {'jobseeker_id': self.kwargs['jobseeker_id']}


class LanguageTitleViewSet(ModelViewSet):
    serializer_class = LanguageTitleSerializer
    queryset = LanguageTitle.objects.all()
    

class SoftwareSkillTitleViewSet(ModelViewSet):
    serializer_class = SoftwareSkillTitleSerializer
    queryset = SoftwareSkillTitle.objects \
        .select_related('softwareskillcategory').all()


class SoftwareSkillCategoryViewSet(ModelViewSet):
    queryset = SoftwareSkillCategory.objects.all()
    serializer_class = SoftwareSkillCategorySerializer


# -----------------------------------------------------------
# karfarma

class EmployerViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    serializer_class = EmployerSerializer
    permission_classes = [IsOwnUserOrReadOnlyEmployer, IsAuthenticated]
    def get_queryset(self):
        return Employer.objects \
        .select_related('user') \
        .filter(user_id=self.request.user.id)


class JobDetailViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnUserOrReadOnlyEmployer2]
    serializer_class = JobDetailSerializer
    
    def get_queryset(self):
        return JobDetail.objects \
            .filter(employer__user_id=self.request.user.id) \
            .select_related('employer', 'field_of_Study')

    def get_serializer_context(self):
        return {'employer_pk': self.kwargs['employer_pk']}

 
class JobDetailAllUserViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = JobDetail.objects.all() \
        .select_related('employer', 'field_of_Study')
    serializer_class = JobDetailAllUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
                       'created_at', 'salary']
    search_fields = ['job_title']
    filterset_fields = ['organizational_category', 'attract_an_intern', 
                       'attracting_the_disabled', 'the_amount_of_work_experience']
    pagination_class = DefaultPagination
   
        
        
class FieldOfStudyViewSet(ModelViewSet):
    queryset = FieldOfStudy.objects.all()
    serializer_class = FieldOfStudySerializer
    
    
class BasicInformationOfOrganizationViewSet(ModelViewSet):
    permission_classes = [IsOwnUserOrReadOnlyEmployer2, IsAuthenticated]
    serializer_class = BasicInformationOfOrganizationSerializer
    
    def get_queryset(self):
        return BasicInformationOfOrganization.objects \
            .filter(employer__user_id=self.request.user.employer.id) \
            .select_related('employer', 'city', 'state')
    
    def get_serializer_context(self):
        return {'employer_id': self.kwargs['employer_pk']}
 
 
class BasicInformationOfOrganizationAllUserViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = BasicInformationOfOrganization.objects.all() \
        .select_related('employer', 'city', 'state')
    serializer_class = BasicInformationOfOrganizationSerializer

    
class EmployerLanguageViewSet(ModelViewSet):
    serializer_class = EmployerLanguageSerializer
    
    def get_queryset(self):
        return Language.objects.select_related('languagetitle','jobdetail') \
            .filter(jobdetail__employer__user_id=self.request.user.employer.id)

    def get_serializer_context(self):
        return {'employer_id': self.kwargs['employer_pk']}
 
 
class EmployerSoftwareSkillViewSet(ModelViewSet):
    serializer_class = EmployerSoftwareSkillSerializer

    def get_queryset(self):
        return SoftwareSkill.objects \
            .filter(jobdetail__employer__user_id=self.request.user.employer.id) \
            .order_by('id').select_related('softwareskillcategory' ,'title' ,'jobdetail')
    
    def get_serializer_context(self):
        return {'employer_id': self.request.user.employer.id}

class ApplicantViewSet(ModelViewSet):
    serializer_class = JobSeekerApplicantSerializer
    
    def get_queryset(self):
        return Applicant.objects \
            .select_related('jobseeker', 'jobdetail') \
            .filter(jobseeker__user_id=self.request.user.id)
            
    def get_serializer_context(self):
        return {'jobseeker_id': self.request.user.jobseeker.id}


class EmployerApplicantViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    
    serializer_class = EmployerApplicantSerializer
    
    def get_queryset(self):
        return Applicant.objects \
            .select_related('jobseeker', 'jobdetail') \
            .filter(jobdetail__employer__user_id=self.request.user.id)
            
    def get_serializer_context(self):
        return {'jobdetail_id': self.request.user.employer.jobdetail_set}

