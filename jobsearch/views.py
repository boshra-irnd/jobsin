from re import search

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
import urllib3
from .models import (Employee, Language, SoftwareSkill,WorkExperience,
                     JobCategory, EducationalBackground, LanguageTitle, 
                     SoftwareSkillTitle, SoftwareSkillCategory)
from .serializers import (EmployeeSerializer, SoftwareSkillSerializer,
                          LanguageSerializer, EducationalBackgroundSerializer, StateSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer,
                          LanguageTitleSerializer, SoftwareSkillCategorySerializer,
                          SoftwareSkillTitleSerializer)
from rest_framework.permissions import (AllowAny, DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly,
                                        IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import (IsAdminOrReadOnly, IsOwnUserOrReadOnly2, IsOwnUserOrReadOnly)
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination

# Create your views here.

class EmployeeViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete']
    queryset = Employee.objects.select_related('user', 'Preferred_job_category', 'state', 'city').all()
    pagination_class = DefaultPagination
    serializer_class = EmployeeSerializer
    # permission_classes = [IsOwnUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['date_of_birth']
    search_fields = ['employee_educationalbackground__university']
    # filterset_fields = ['Preferred_job_category', 
    #                     'employee_educationalbackground__degree_level',
    #                     'gender', 'state', 'city']
    lookup_url_kwarg = "id"
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsOwnUserOrReadOnly])
    def me(self, request):
        employee = Employee.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = EmployeeSerializer(employee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SoftwareSkillViewset(ModelViewSet):
    serializer_class = SoftwareSkillSerializer
    permission_classes = [IsOwnUserOrReadOnly2]

    def get_queryset(self):
        return SoftwareSkill.objects.filter(employee_id=self.kwargs['employee_id']).order_by('id').select_related('softwareskillcategory').select_related('title')
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}

  
class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    
    def get_queryset(self):
        return Language.objects.select_related('languagetitle').filter(employee_id=self.kwargs['employee_id'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}
    
    
class WorkExperienceViewSet(ModelViewSet):
    serializer_class = WorkExperienceSerializer
    
    def get_queryset(self):
        return WorkExperience.objects.filter(employee_id=self.kwargs['employee_id']).select_related('state')
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}


class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    

class EducationalBackgroundViewSet(ModelViewSet):
    serializer_class = EducationalBackgroundSerializer
    
    def get_queryset(self):
        return EducationalBackground.objects.filter(employee_id=self.kwargs['employee_id'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}


class LanguageTitleViewSet(ModelViewSet):
    serializer_class = LanguageTitleSerializer
    queryset = LanguageTitle.objects.all()
    

class SoftwareSkillTitleViewSet(ModelViewSet):
    serializer_class = SoftwareSkillTitleSerializer
    queryset = SoftwareSkillTitle.objects.all()


class SoftwareSkillCategoryViewSet(ModelViewSet):
    queryset = SoftwareSkillCategory.objects.all()
    serializer_class = SoftwareSkillCategorySerializer
