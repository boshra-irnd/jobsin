from cgitb import lookup
from posixpath import basename
from django.urls import path
from rest_framework_nested import routers
from .views import (JobCategoryViewSet, EmployeeViewSet,
                    LanguagesViewSet, SoftwareSkillViewset, WorkExperienceViewSet,
                    EducationalBackgroundViewSet) 



router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet)
router.register(r'jobcategory', JobCategoryViewSet)

employee_router = routers.NestedDefaultRouter(router, 'employee', lookup='employee')

employee_router.register('languages', LanguagesViewSet, basename='employee-language')
employee_router.register('educationalbackground', EducationalBackgroundViewSet, basename='employee-educationalbackground')
employee_router.register('workexperience', WorkExperienceViewSet, basename='employee-workexperience')
employee_router.register('softwareskill', SoftwareSkillViewset, basename='employee-softwareskill')

urlpatterns = router.urls + employee_router.urls