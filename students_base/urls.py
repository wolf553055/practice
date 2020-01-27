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
]

