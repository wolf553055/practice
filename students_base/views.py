from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from .forms import *


def check_vacancy():
    sch = 0
    vacancy = []
    v_s = []
    vac = Vacancy.objects.order_by("title")
    people = Job.objects.order_by("fio")
    vac_list = []
    for el in vac:
        vac_list.append([el, el.skills_vacancy_set.all()])
    st_list = []
    for el in people:
        st_list.append([el, el.skills_student_set.all()])
    for el, value in st_list:
        for el_v, value_v in vac_list:
            if not el_v.worker:
                for key in value:
                    for key_v in value_v:
                        if str(key) == str(key_v):
                            sch += 1
                if sch != 0:
                    vacancy.append([el_v, value_v])
                    sch = 0
        if vacancy:
            v_s.append([el, value, vacancy])
        else:
            v_s.append([el, value, []])
        vacancy = []
    return v_s


class Index(View):
    template = 'index.html'

    def get(self, request):
        st_list = check_vacancy()
        list_employments = List_of_employment.objects.order_by("employment")
        context = {
            'form': PersonForm(),
            'list_employments': list_employments,
            'st_list': st_list,
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