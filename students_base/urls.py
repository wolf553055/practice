from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('vacancy/', VacPage.as_view(), name='vacancy'),
    path('vacancy_skills/', VacSkPage.as_view(), name='vacancy_skills')
]