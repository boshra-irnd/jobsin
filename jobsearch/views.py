from urllib import response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import (Employee, Address, Languages, SoftwareSkills,
                     WorkExperience, JobCategory, EducationalBackground)
from .serializers import (EmployeeSerializer, AddressSerializer, SoftwareSkillSerializer,
                          LanguagesSerializer, EducationalBackgroundSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer)
from jobsearch import permissions, serializers
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly
# Create your views here.

class EmployeeViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (employee, created) = Employee.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = EmployeeSerializer(employee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
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
    serializer_class = JobCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class EducationalBackgroundViewSet(ModelViewSet):
    queryset = EducationalBackground.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = EducationalBackgroundSerializer