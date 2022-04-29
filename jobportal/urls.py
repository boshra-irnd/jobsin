from cgitb import lookup
from posixpath import basename
from django.urls import path
from rest_framework_nested import routers
from .views import (JobCategoryViewSet, JobSeekerViewSet,JobSeekerLanguageViewSet,
                    EducationalBackgroundViewSet, EmployerViewSet,JobSeekerSoftwareSkillViewSet, 
                    BasicInformationOfOrganizationViewSet,JobDetailViewSet,FieldOfStudyViewSet,
                    WorkExperienceViewSet, EmployerLanguageViewSet,JobDetailAllUserViewSet,
                    BasicInformationOfOrganizationAllUserViewSet, EmployerSoftwareSkillViewSet,
                    ApplicantViewSet, EmployerApplicantViewSet) 



router = routers.DefaultRouter()
router.register(r'employer', EmployerViewSet, basename='employer')
employer_router = routers.NestedDefaultRouter(router, 'employer', lookup='employer')
router.register(r'jobseeker', JobSeekerViewSet, basename='jobseeker')
router.register(r'basicinformationall', BasicInformationOfOrganizationAllUserViewSet, basename='basicinformation')
router.register(r'jobdetailall', JobDetailAllUserViewSet, basename='jobdetailall')


employer_router.register('jobdetail', JobDetailViewSet, basename='jobdetail')
employer_router.register('jd_language', EmployerLanguageViewSet, basename='jd_language')
employer_router.register('basicinformation', BasicInformationOfOrganizationViewSet, basename='basicinformation')
employer_router.register('jd_softwareskill', EmployerSoftwareSkillViewSet, basename='jd_softwareskill')
employer_router.register('jd_applicant', EmployerApplicantViewSet, basename='jd_softwareskill')

jobseeker_router = routers.NestedDefaultRouter(router, 'jobseeker', lookup='jobseeker')
jobseeker_router.register('languages', JobSeekerLanguageViewSet, basename='jobseeker-language')
jobseeker_router.register('educationalbackground', EducationalBackgroundViewSet, basename='jobseeker-educationalbackground')
jobseeker_router.register('workexperience', WorkExperienceViewSet, basename='jobseeker-workexperience')
jobseeker_router.register('softwareskill', JobSeekerSoftwareSkillViewSet, basename='jobseeker-softwareskill')
jobseeker_router.register('applicant', ApplicantViewSet, basename='jobseeker-applicant')



urlpatterns = router.urls + jobseeker_router.urls + employer_router.urls
