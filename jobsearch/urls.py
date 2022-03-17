from cgitb import lookup
from posixpath import basename
from django.urls import path
from rest_framework_nested import routers
from .views import (JobCategoryViewSet, AddressViewSet, EmployeeViewSet,
                    LanguagesViewSet, SoftwareSkillViewset, WorkExperienceViewSet,
                    EducationalBackgroundViewSet) 



router = routers.SimpleRouter()
router.register(r'employee', EmployeeViewSet)
router.register(r'jobcategory', JobCategoryViewSet)
router.register(r'address', AddressViewSet, basename='address')
router.register(r'language', LanguagesViewSet)
router.register(r'softwareskill', SoftwareSkillViewset)
router.register(r'workexperience', WorkExperienceViewSet)
router.register(r'educationalbackground', EducationalBackgroundViewSet)
employee_router = routers.NestedDefaultRouter(router, 'employee', lookup='employee')
employee_router.register('address', AddressViewSet, basename='employees-address')

urlpatterns = router.urls + employee_router.urls