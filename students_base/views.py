import datetime
import xlwt
import xlrd

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from xlwt.compat import xrange
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from django.views.generic import View
from .forms import *


def check_calls(person):
    for call in person.calls_set.order_by('-call_time').filter(call_time__lte=datetime.datetime.now()):
        if call.status != 'Завершён':
            call.status = 'Истёк'
            call.save()


@method_decorator(login_required, name='dispatch')
class Index(View):
    template = 'index.html'

    def get(self, request):
        people = Job.objects.order_by("fio")
        list_employments = List_of_employment.objects.order_by("employment")
        for person in people:
            check_calls(person)
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
        try:
            el = List_of_employment.objects.get(employment=is_employment)
            color = el.color
        except:
            el = List_of_employment()
            el.employment = is_employment
            el.save()
            color = None
        if bound_form.is_valid():
            bound_form.save()
            people = Job.objects.filter(employment=is_employment)
            for person in people:
                person.color = color
                person.save()
            return redirect('/students_base')
        else:
            print(bound_form.errors)
        context = {
            'form': bound_form
        }
        return render(request, self.template, context)


@method_decorator(login_required, name='dispatch')
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
            return redirect('/students_base/student_detail/' + str(student.id))
        return HttpResponse(status=404)


class AddVacancy(View):
    def post(self, request):
        vacancy = request.POST.get("vacancy")
        id_st = request.POST.get("id_st")
        student = Job.objects.get(id=id_st)
        try:
            vac = Vacancy.objects.get(id=vacancy)
            if request.method == 'POST':
                student.vacancy_st = vac.title
                student.on_speciality = 'По специальности'
                student.save()
                vac.worker = student
                vac.save()
                return redirect('/students_base/student_detail/' + str(student.id))
        except ValueError:
            return HttpResponse(status=404)


class AddOrganization(View):
    def post(self, request):
        bound_form = OrganizationForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/vacancy')
        return HttpResponse(status=404)


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
        return HttpResponse(status=404)


class AddDocument(View):
    def post(self, request):
        expansions = ['jpg', 'jpeg', 'png']
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                worker = Job.objects.get(id=request.POST['worker'])
                newimg = DocumentImg(document=request.FILES['docfile'], worker=worker,
                                     title=request.POST['title'])
                expansion = str(request.FILES['docfile']).split(".")[1]
                newimg.type = 'Картинка' if expansion in expansions else 'Документ'
                newimg.save()
                return redirect('/students_base/')
            else:
                return HttpResponse(status=404)


@method_decorator(login_required, name='dispatch')
class StudentDetail(View):
    template = 'student_detail.html'

    def check_vacancy(self, person):
        vacancy_p = []
        sch = 0
        vacancy = Vacancy.objects.order_by("title")
        people = Job.objects.order_by("fio")
        for vac in vacancy:
            if not vac.worker:
                for key in person.skills_student_set.all():
                    for key_v in vac.skills_vacancy_set.all():
                        if str(key) == str(key_v):
                            sch += 1
                if sch != 0:
                    vacancy_p.append(vac)
        return vacancy_p

    def get(self, request, pk):
        person = get_object_or_404(Job, id=pk)
        check_calls(person)
        context = {
            'person': person,
            'call_form': CallsForm(),
            'vacancy': self.check_vacancy(person)
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


@method_decorator(login_required, name='dispatch')
class Education(View):
    template = 'education.html'

    def get(self, request):
        colleges = College.objects.all()
        context = {
            'form': CollegeForm(),
            'colleges': colleges,
            'g_form': GroupForm(),
        }
        return render(request, self.template, context)

    def post(self, request):
        bound_form = CollegeForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/education')
        return HttpResponse(status=404)


class Spec(View):
    def post(self, request):
        if request.method == 'POST':
            college = College.objects.get(id=request.POST.get("college"))
            spec = Specialty()
            spec.title = request.POST.get("title")
            spec.college = college
            spec.save()
            return redirect('/students_base/education')
        return HttpResponse(status=404)


def export_students_xls(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="students.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Студенты')

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = []
        print(request.POST.values())
        fields_dict = request.POST.dict()
        del fields_dict["csrfmiddlewaretoken"]

        for field in fields_dict.values():
            columns.append(field)

        # columns = ['ФИО', 'e-mail', 'телефон', 'форма финансирования',
        #            'трудоустроенность', 'вид занятости']

        for col_num in xrange(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = []
        for student in Job.objects.all():
            student_info = []
            if request.POST.get("fio_check") is not None:
                student_info.append(student.fio)
            if request.POST.get("release_year_check") is not None:
                student_info.append(student.release_year)
            if request.POST.get("employment_check") is not None:
                if student.expiry_date is not None:
                    student_info.append(student.employment + str(student.expiry_date))
                else:
                    student_info.append(student.employment)
            if request.POST.get("specialty_check") is not None:
                student_info.append(student.specialty.title)
            if request.POST.get("practice_one_check") is not None:
                student_info.append(student.practice_one)
            if request.POST.get("practice_two_check") is not None:
                student_info.append(student.practice_two)
            if request.POST.get("vacancy_st_check") is not None:
                if student.vacancy_st is not None:
                    student_info.append(student.vacancy_st)
                else:
                    student_info.append("Безработный")
            if request.POST.get("on_speciality_check") is not None:
                student_info.append(student.on_speciality)
            rows.append(student_info)

        # rows = Job.objects.all().values_list('fio', 'email', 'phone_number',
        #                                      'budget', 'vacancy_st', 'on_speciality')
        for row in rows:
            row_num += 1
            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response


def import_students_excel(request):
    if request.method == 'POST':
        filename = request.FILES['filename']
        file_import = xlrd.open_workbook(file_contents=filename.read())
        sheet = file_import.sheet_by_index(0)
        for rownum in range(sheet.nrows):
            student = Job()
            student.fio = sheet.row_values(rownum)[0]
            student.release_year = datetime.datetime(
                *xlrd.xldate_as_tuple(sheet.row_values(rownum)[1], file_import.datemode)).strftime('%d.%m.%Y')
            student.budget = sheet.row_values(rownum)[2]
            student.practice_one = sheet.row_values(rownum)[3]
            student.practice_two = sheet.row_values(rownum)[4]
            student.phone_number = sheet.row_values(rownum)[5]
            student.email = sheet.row_values(rownum)[6]
            student.employment = sheet.row_values(rownum)[7].split("|")[0]
            if len(sheet.row_values(rownum)[7].split("|")) > 1:
                date = sheet.row_values(rownum)[7].split("|")[1]
                student.expiry_date = datetime.datetime.strptime(date, "%d.%m.%Y")
            coll = College.objects.get(title=sheet.row_values(rownum)[10])
            print(sheet.row_values(rownum)[9])
            spec = coll.specialty_set.get(title=sheet.row_values(rownum)[9])
            gr = spec.group_set.get(title=sheet.row_values(rownum)[8])
            student.specialty = gr
            if len(sheet.row_values(rownum)) == 13:
                if sheet.row_values(rownum)[11]:
                    student.vacancy_st = sheet.row_values(rownum)[11]
                    student.on_speciality = sheet.row_values(rownum)[12]
            student.save()
        return redirect('/students_base/')


class AddGroup(View):
    def post(self, request):
        bound_form = GroupForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('/students_base/education')
        return HttpResponse(status=404)


@method_decorator(login_required, name='dispatch')
class Settings(View):
    template = 'settings.html'

    def get(self, request):
        employments = List_of_employment.objects.all()
        context = {
            'employments': employments,
        }
        return render(request, self.template, context)

    def post(self, request):
        if request.method == 'POST':
            employment = get_object_or_404(List_of_employment, id=request.POST.get("employment"))
            employment.color = request.POST.get("color")
            employment.save()
            people = Job.objects.filter(employment=employment)
            for person in people:
                person.color = employment.color
                person.save()
            return redirect('/students_base/settings/')


@method_decorator(login_required, name='dispatch')
class Documentation(View):
    template = "documentation.html"

    def get(self, request):
        context = {
            'title': 'Документация',
        }
        return render(request, self.template, context)
