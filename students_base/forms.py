from django import forms
from .models import *
from django.forms import inlineformset_factory


class PersonForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['fio', 'release_year', 'budget', 'code',
                  'practice_one', 'practice_two', 'employment']
        labels = {
            'fio': 'ФИО',
            'release_year': 'Дата рождения',
            'employment': 'Занятость',
            'code': 'Шифр / Наименование специальности',
            'practice_one': 'Место прохождения первой практики',
            'practice_two': 'Место прохождения второй практики',
            'budget': 'Бюджет / Платник',
        }
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'release_year': forms.TextInput(attrs={'class': 'form-control', 'id': 'date_of_birth'}),
            'speciality': forms.TextInput(attrs={'class': 'form-control'}),
            'employment': forms.TextInput(attrs={'class': 'form-control', 'id': 'employment'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'id': 'code_spec'}),
            'practice_one': forms.TextInput(attrs={'class': 'form-control'}),
            'practice_two': forms.TextInput(attrs={'class': 'form-control'}),
            'budget': forms.RadioSelect(),
        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'
        labels = {
            'title': 'Название вакансии',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class VacancySkillsForm(forms.ModelForm):
    class Meta:
        model = Skills_Vacancy
        fields = '__all__'
        labels = {
            'vacancy': 'Название вакансии',
            'title': 'Что должен уметь'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        labels = {
            'title': 'Название организации'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
