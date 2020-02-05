from django import forms
from .models import *


class PersonForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['fio', 'release_year', 'budget', 'code',
                  'practice_one', 'practice_two', 'phone_number', 'email', 'employment']
        labels = {
            'fio': 'ФИО',
            'release_year': 'Дата рождения',
            'employment': 'Занятость',
            'code': 'Шифр / Наименование специальности',
            'practice_one': 'Место прохождения первой практики',
            'practice_two': 'Место прохождения второй практики',
            'budget': 'Бюджет / Платник',
            'phone_number': 'Номер телефона',
            'email': 'Электронная почта',
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
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'phone_number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
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


class ImageForm(forms.Form):
    docfile = forms.FileField(
        label='Добавить документ',
        help_text='max. 42 megabytes'
    )


class CallsForm(forms.ModelForm):
    class Meta:
        model = Calls
        fields = '__all__'
        widgets = {
            'call_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }
