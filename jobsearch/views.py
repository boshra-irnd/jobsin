from re import search

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
import urllib3
from .models import (Employee, Languages, SoftwareSkills,
                     WorkExperience, JobCategory, EducationalBackground)
from .serializers import (EmployeeSerializer, SoftwareSkillSerializer,
                          LanguagesSerializer, EducationalBackgroundSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer)
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnUserOrReadOnly2, IsOwnUserOrReadOnly, IsOwnUserOrReadOnly3
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
from rest_framework import permissions
import urllib
# Create your views here.

class EmployeeViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete']
    queryset = Employee.objects.all()
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
   
# # jhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
# class CheckParentPermissionMixin:
#     parent_queryset: Employee.objects.all()
#     parent_lookup_field: 'id'
#     parent_lookup_url_kwarg: 'id'

#     def __init__(self, **kwargs):
#         self.parent_obj: Any = None
#         super().__init__(**kwargs)

#     def check_permissions(self, request):
#         super().check_permissions(request)

#         # check permissions for the parent object
#         parent_lookup_url_kwarg = self.parent_lookup_url_kwarg or self.parent_lookup_field
#         filter_kwargs = {
#             self.parent_lookup_field: kwargs[parent_lookup_url_kwarg]
#         }
#         self.parent_obj = get_object_or_404(self.parent_queryset, **filter_kwargs)
#         self.parent_obj._is_parent_obj = True
#         super().check_object_permissions(request, self.parent_obj)


class SoftwareSkillViewset(CheckParentPermissionMixin,ModelViewSet):
    serializer_class = SoftwareSkillSerializer
    permission_classes = [IsOwnUserOrReadOnly2]
    # parent_queryset = Employee.objects.all()
    # parent_lookup_field = 'id'
    # parent_lookup_url_kwarg = 'id'
    # lookup_field = 'id'
    def dispatch(self, request, *args, **kwargs):
        parent_view = EmployeeViewSet.as_view({'get':'retrieve'})
        original_method = 'GET'
        parent_kwargs = {'id':kwargs['employee_id']}
        
        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response
        request.method = original_method
        return super().dispatch(request, *args, **kwargs)    
    
    def get_queryset(self):
        return SoftwareSkills.objects.filter(employee_id=self.kwargs['employee_id'])
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}

  
class LanguagesViewSet(ModelViewSet):
    serializer_class = LanguagesSerializer
    permission_classes = [IsAdminOrReadOnly]
    
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
  