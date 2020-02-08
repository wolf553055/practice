import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import View
from .forms import *


def check_vacancy():
    people_vac = []
    vacancy_p = []
    sch = 0
    vacancy = Vacancy.objects.order_by("title")
    people = Job.objects.order_by("fio")
    for person in people:
        for vac in vacancy:
            if not vac.worker:
                for key in person.skills_student_set.all():
                    for key_v in vac.skills_vacancy_set.all():
                        if str(key) == str(key_v):
                            sch += 1
                if sch != 0:
                    vacancy_p.append(vac)
                    sch = 0
        if vacancy:
            people_vac.append([person, vacancy_p])
        vacancy_p = []
    return people_vac


class Index(View):
    template = 'index.html'

    def check_notifications(self, people):
        for person, vacancy in people:
            sch = 0
            for calls in person.calls_set.all():
                if calls.status == 'Истёк':
                    sch += 1
            person.notifications = sch

    def get(self, request):
        people = check_vacancy()
        self.check_notifications(people)
        list_employments = List_of_employment.objects.order_by("employment")
        context = {
            'form': PersonForm(),
            'list_employments': list_employments,
            'people': people,
            'imgform': ImageForm,
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
        else:
            print(bound_form.errors)
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
            if request.method == 'POST':
                student.vacancy_st = vac.title
                student.save()
                vac.worker = student
                vac.save()
                return redirect('/students_base/')
        except ValueError:
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


class AddDocument(View):
    def post(self, request):
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                worker = Job.objects.get(id=request.POST['worker'])
                newimg = DocumentImg(document=request.FILES['docfile'], worker=worker,
                                     title=request.POST['title'])
                newimg.save()
                return redirect('/students_base/')
            else:
                return redirect('/students_base/')


class StudentDetail(View):
    template = 'student_detail.html'

    def check_calls(self, person):
        for call in person.calls_set.order_by('-call_time').filter(call_time__lte=datetime.datetime.now()):
            if call.status != 'Завершён':
                call.status = 'Истёк'
                call.save()

    def get(self, request, pk):
        person = get_object_or_404(Job, id=pk)
        self.check_calls(person)
        context = {
            'person': person,
            'call_form': CallsForm(),
        }
        return render(request, self.template, context)

    def post(self, request, pk):
        person = get_object_or_404(Job, id=pk)
        context = {
            'person': person,
            'call_form': CallsForm()
        }
        if request.method == 'POST':
            time = request.POST.get("call_time").split("T")
            call = Calls()
            call.call_time = ("{} {}").format(time[0], time[1])
            call.comment = request.POST.get("comment")
            call.fio = person
            call.status = 'В процессе'
            call.save()
        return redirect('/students_base/student_detail/' + str(person.id))


class CancleCalls(View):
    def post(self, request, pk):
        if request.method == 'POST':
            call = get_object_or_404(Calls, id=pk)
            call.status = request.POST.get("status")
            call.save()
            return redirect('/students_base/student_detail/' + str(call.fio.id))


class Education(View):
    template = 'education.html'

    def get(self, request):
        colleges = College.objects.all()
        context = {
            'form': CollegeForm(),
            'colleges': colleges,
        }
        return render(request, self.template, context)

    def post(self, request):
        bound_form = CollegeForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/education')
        return redirect('/students_base/education')


class Spec(View):
    def post(self, request):
        if request.method == 'POST':
            college = College.objects.get(id=request.POST.get("college"))
            spec = Specialty()
            spec.title = request.POST.get("title")
            spec.college = college
            spec.save()
            return redirect('/students_base/education')
        return redirect('/students_base/education')
