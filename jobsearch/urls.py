from cgitb import lookup
from posixpath import basename
from django.urls import path
from rest_framework_nested import routers
from .views import (JobCategoryViewSet, EmployeeViewSet,JobSeekerLanguageViewSet,
                    EducationalBackgroundViewSet, EmployerViewSet,EmployeeSoftwareSkillViewSet, 
                    BasicInformationOfOrganizationViewSet,JobDetailViewSet,FieldOfStudyViewSet,
                    WorkExperienceViewSet, EmployerLanguageViewSet,JobDetailAllUserViewSet,
                    BasicInformationOfOrganizationAllUserViewSet, EmployerSoftwareSkillViewSet) 



router = routers.DefaultRouter()
router.register(r'employer', EmployerViewSet, basename='employer')
employer_router = routers.NestedDefaultRouter(router, 'employer', lookup='employer')
router.register(r'employee', EmployeeViewSet, basename='jobsearch')
router.register(r'basicinformationall', BasicInformationOfOrganizationAllUserViewSet, basename='basicinformation')
router.register(r'jobdetailall', JobDetailAllUserViewSet, basename='jobdetailall')


employer_router.register('jobdetail', JobDetailViewSet, basename='jobdetail')
employer_router.register('jd_language', EmployerLanguageViewSet, basename='jd_language')
employer_router.register('basicinformation', BasicInformationOfOrganizationViewSet, basename='basicinformation')
employer_router.register('jd_softwareskill', EmployerSoftwareSkillViewSet, basename='jd_softwareskill')

employee_router = routers.NestedDefaultRouter(router, 'employee', lookup='employee')
employee_router.register('languages', JobSeekerLanguageViewSet, basename='employee-language')
employee_router.register('educationalbackground', EducationalBackgroundViewSet, basename='employee-educationalbackground')
employee_router.register('workexperience', WorkExperienceViewSet, basename='employee-workexperience')
employee_router.register('softwareskill', EmployeeSoftwareSkillViewSet, basename='employee-softwareskill')



urlpatterns = router.urls + employee_router.urls + employer_router.urls
