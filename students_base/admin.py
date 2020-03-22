from django.contrib import admin
from .models import *

# Регистрация моделей в админ панели
admin.site.register(Job)  # модель студентов
admin.site.register(Organization)  # модель организаций
admin.site.register(Vacancy)  # модель вакансий
admin.site.register(College)  # модель учебных заведений
admin.site.register(Specialty)  # модель специальностей
admin.site.register(Group)  # модель групп
