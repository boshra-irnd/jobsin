import imp
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import (Employee, Address, Languages, SoftwareSkills,
                     WorkExperience, JobCategory, EducationalBackground)
from .serializers import (EmployeeSerializer, AddressSerializer, SoftwareSkillSerializer,
                          LanguagesSerializer, EducationalBackgroundSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer)
from jobsearch import serializers
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
# Create your views here.

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        return Address.objects.get(employee_id=self.kwargs['employee_pk'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_pk']}
    
    
class SoftwareSkillViewset(ModelViewSet):
    queryset = SoftwareSkills.objects.all()
    serializer_class = SoftwareSkillSerializer
    
class LanguagesViewSet(ModelViewSet):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer
    
class WorkExperienceViewSet(ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    
class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = JobCategorySerializer

class EducationalBackgroundViewSet(ModelViewSet):
    queryset = EducationalBackground.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = EducationalBackgroundSerializer