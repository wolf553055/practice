from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from .forms import *


def check_vacancy():
    people_vac = []
    vacancy_p = []
    vacancy = Vacancy.objects.order_by("title")
    people = Job.objects.order_by("fio")
    for person in people:
        for vac in vacancy:
            if list(set(person.skills_student_set.all()) - set(vac.skills_vacancy_set.all())) and not vac.worker:
                vacancy_p.append(vac)
        people_vac.append([person, vacancy_p])
        vacancy_p = []
    return people_vac


class Index(View):
    template = 'index.html'

    def get(self, request):
        people = check_vacancy()
        list_employments = List_of_employment.objects.order_by("employment")
        context = {
            'form': PersonForm(),
            'list_employments': list_employments,
            'people': people,
        }
        return render(request, self.template, context)

    def post(self, request):
        bound_form = PersonForm(request.POST)
        is_employment = request.POST.get("employment")
        el = List_of_employment.objects.filter(employment=is_employment)
        if not el:
            em = List_of_employment()
            em.employment = is_employment
            em.save()
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base')
        context = {
            'form': bound_form
        }
        return render(request, self.template, context)


class VacPage(View):
    template = 'vacancy.html'

    def get(self, request):
        org = Organization.objects.order_by("title")
        context = {
            'form_org': OrganizationForm(),
            'org_list': org
        }
        return render(request, self.template, context)

    def post(self, request):
        bound_form = VacancyForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/vacancy')
        context = {
            'form': bound_form
        }
        return render(request, self.template, context)


class VacSkPage(View):
    def post(self, request):
        if request.method == 'POST':
            sk_vac = Skills_Vacancy()
            sk_vac.title = request.POST.get("title")
            vac_id = request.POST.get("vacancy")
            vac = Vacancy.objects.get(id=vac_id)
            sk_vac.vacancy = vac
            sk_vac.save()
        return redirect('/students_base/vacancy')


class StSkPage(View):
    def post(self, request):
        id_st = request.POST.get("id")
        student = Job.objects.get(id=id_st)
        if request.method == 'POST':
            st_skills = Skills_Student()
            st_skills.fio = student
            st_skills.title = request.POST.get("title")
            st_skills.save()
            return redirect('/students_base/')
        return redirect('/students_base/')


class AddVacancy(View):
    def post(self, request):
        vacancy = request.POST.get("vacancy")
        id_st = request.POST.get("id_st")
        student = Job.objects.get(id=id_st)
        try:
            vac = Vacancy.objects.get(id=vacancy)
            print(vac.worker)
            if request.method == 'POST':
                student.vacancy_st = vac.title
                student.save()
                vac.worker = student
                vac.save()
                return redirect('/students_base/')
        except ValueError:
            print("lol")
            return redirect('/students_base/')


class AddOrganization(View):
    def post(self, request):
        bound_form = OrganizationForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/vacancy')
        return redirect('/students_base/vacancy')


class AddVacancyOrganization(View):
    def post(self, request):
        if request.method == 'POST':
            vacancy = Vacancy()
            vacancy.title = request.POST.get("title")
            organization_id = request.POST.get("organization")
            organization = Organization.objects.get(id=organization_id)
            vacancy.organization = organization
            vacancy.save()
            return redirect('/students_base/vacancy')
        return redirect('/students_base/vacancy')
