from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Job, List_of_employment, Vacancy, Skills_Vacancy
from django.views.generic import View
from .forms import PersonForm, VacancyForm, VacancySkillsForm


class Index(View):
    template = 'index.html'

    def get(self, request):
        people = Job.objects.order_by("fio")
        list_employments = List_of_employment.objects.order_by("employment")
        context = {
            'people': people,
            'form': PersonForm(),
            'list_employments': list_employments,
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
        vac = Vacancy.objects.order_by("title")
        vac_list = []
        for el in vac:
            vac_list.append([el, el.skills_vacancy_set.all()])
        context = {
            'vac': vac,
            'vac_sk': vac_list,
            'form_sk': VacancySkillsForm(),
            'form_v': VacancyForm()
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
        bound_form = VacancySkillsForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/vacancy')
        return redirect('/students_base/vacancy')