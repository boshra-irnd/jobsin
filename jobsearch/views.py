from re import search
from rest_framework.viewsets import ModelViewSet
from .models import (Employee, Languages, SoftwareSkills,
                     WorkExperience, JobCategory, EducationalBackground)
from .serializers import (EmployeeSerializer, SoftwareSkillSerializer,
                          LanguagesSerializer, EducationalBackgroundSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer)
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
# Create your views here.

class EmployeeViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['date_of_birth']
    search_fields = ['employee_educationalbackground__university']
    filterset_fields = ['Preferred_job_category', 
                        'employee_educationalbackground__degree_level',
                        'gender', 'state', 'city']

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
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
    
    def get_queryset(self):
        return SoftwareSkills.objects.filter(employee_id=self.kwargs['employee_pk'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}
    
    
    
class LanguagesViewSet(ModelViewSet):
    serializer_class = LanguagesSerializer
    
    def get_queryset(self):
        return Languages.objects.filter(employee_id=self.kwargs['employee_pk'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}
    
    
class WorkExperienceViewSet(ModelViewSet):
    serializer_class = WorkExperienceSerializer
    
    def get_queryset(self):
        return WorkExperience.objects.filter(employee_id=self.kwargs['employee_pk'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}

class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    

class EducationalBackgroundViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = EducationalBackgroundSerializer
    
    def get_queryset(self):
        return EducationalBackground.objects.filter(employee_id=self.kwargs['employee_pk'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}
  