from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import mixins, generics
from rest_framework.permissions import (AllowAny, DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly,
                                        IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import (IsAdminOrReadOnly, IsOwnUserOrReadOnly2, IsOwnUserOrReadOnly)
from .pagination import DefaultPagination
from .serializers import (EmployeeSerializer, SoftwareSkillSerializer,
                          LanguageSerializer, EducationalBackgroundSerializer, StateSerializer, 
                          WorkExperienceSerializer, JobCategorySerializer,
                          LanguageTitleSerializer, SoftwareSkillCategorySerializer,
                          SoftwareSkillTitleSerializer)
from .models import (Employee, Language, SoftwareSkill,WorkExperience,
                     JobCategory, EducationalBackground, LanguageTitle, 
                     SoftwareSkillTitle, SoftwareSkillCategory)

# Create your views here.

class EmployeeViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
    lookup_url_kwarg = "id"
    permission_classes = [IsOwnUserOrReadOnly]
    pagination_class = DefaultPagination
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['date_of_birth']
    # search_fields = ['employee_educationalbackground__university']
    # filterset_fields = ['Preferred_job_category', 
    #                     'employee_educationalbackground__degree_level',
    #                     'gender', 'state', 'city']
    
    
    def get_queryset(self):
        return Employee.objects \
        .select_related('user', 'Preferred_job_category', 'state', 'city') \
        .filter(id=self.request.user.employee.id)
    
    # @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsOwnUserOrReadOnly])
    # def me(self, request):
    #     employee = Employee.objects.get(user_id=request.user.id)
    #     if request.method == 'GET':
    #         serializer = EmployeeSerializer(employee)
    #         return Response(serializer.data)
    #     elif request.method == 'PUT':
    #         serializer = EmployeeSerializer(employee, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)


class SoftwareSkillViewset(ModelViewSet):
    serializer_class = SoftwareSkillSerializer

    def dispatch(self, request, *args, **kwargs):
        parent_view = EmployeeViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["employee_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        return SoftwareSkill.objects \
            .filter(employee__user_id=self.request.user.employee.id) \
            .order_by('id').select_related('employee','softwareskillcategory','title')
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    
    
    def dispatch(self, request, *args, **kwargs):
        parent_view = EmployeeViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["employee_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)

    
    def get_queryset(self):
        return Language.objects.select_related('languagetitle') \
            .filter(employee__user_id=self.request.user.employee.id)
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}
    
    
class WorkExperienceViewSet(ModelViewSet):
    serializer_class = WorkExperienceSerializer
    
    def dispatch(self, request, *args, **kwargs):
        parent_view = EmployeeViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["employee_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)

    
    def get_queryset(self):
        return WorkExperience.objects \
            .filter(employee__user_id=self.request.user.employee.id) \
            .select_related('state')
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}



class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    

class EducationalBackgroundViewSet(ModelViewSet):
    serializer_class = EducationalBackgroundSerializer
    
    def dispatch(self, request, *args, **kwargs):
        parent_view = EmployeeViewSet.as_view({"get": "retrieve"})
        original_method = request.method
        request.method = "GET"
        parent_kwargs = {"id": kwargs["employee_id"]}

        parent_response = parent_view(request, *args, **parent_kwargs)
        if parent_response.exception:
            return parent_response

        request.method = original_method
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return EducationalBackground.objects \
            .filter(employee__user_id=self.request.user.employee.id)
    
    def get_serializer_context(self):
        return {'employee_id': self.kwargs['employee_id']}


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
