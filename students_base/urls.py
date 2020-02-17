from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('vacancy/', VacPage.as_view(), name='vacancy'),
    path('vacancy_skills/', VacSkPage.as_view(), name='vacancy_skills'),
    path('student_skills/', StSkPage.as_view(), name='student_skills'),
    path('add_vacancy/', AddVacancy.as_view(), name='add_vacancy'),
    path('add_org/', AddOrganization.as_view(), name='add_org'),
    path('add_vacancy_org/', AddVacancyOrganization.as_view(), name='add_vacancy_org'),
    path('add_document/', AddDocument.as_view(), name='add_document'),
    path('student_detail/<int:pk>/', StudentDetail.as_view(), name='student_detail'),
    path('calls_cancle/<int:pk>/', CancleCalls.as_view(), name='calls_cancle'),
    path('education/', Education.as_view(), name='education'),
    path('specialty/', Spec.as_view(), name='specialty'),
    path('export/xls/', export_students_xls, name='export_students_xls')
]

