from django.test import TestCase
from django.test import Client

# Create your tests here.
from django.urls import reverse

from .models import College, Specialty, Job, Group
from .forms import PersonForm, ImageForm


class JobModelTest(TestCase):
    """
    Класс для тестирования модели Job
    """

    @classmethod
    def setUpTestData(cls):
        """
        Функция для настройки немодифицированных объектов, используемых всеми методами тестирования
        """
        c = College.objects.create(title='KKMT')
        s = Specialty.objects.create(title='11.11.11 Программирование', college=c)
        g = Group.objects.create(title="П1-17", specialty=s)
        Job.objects.create(fio='Иванов Иван Иванович', release_year='01.01.2015',
                           employment='Уход в армию', specialty=g, practice_one='РКК Энергия',
                           practice_two='РКК Энергия', budget='Бюджет', phone_number='89167819925',
                           email='foo@example.com')

    def test_fio_label(self):
        """
        Функция для тестирования label для поля fio
        """
        student = Job.objects.get(id=1)
        field_label = student._meta.get_field('fio').verbose_name
        self.assertEquals(field_label, 'fio')

    def test_release_year_label(self):
        """
        Функция для тестирования label для поля release_year
        """
        student = Job.objects.get(id=1)
        field_label = student._meta.get_field('release_year').verbose_name
        self.assertEquals(field_label, 'release year')

    def test_fio_max_length(self):
        """
        Функция для тестирования максимальной длинны для поля fio
        """
        student = Job.objects.get(id=1)
        max_length = student._meta.get_field('fio').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        """
        Функция для тестирования поля fio
        """
        student = Job.objects.get(id=1)
        expected_object_name = 'Иванов Иван Иванович'
        self.assertEquals(expected_object_name, str(student))


class PersonFormTest(TestCase):
    """
    Класс для тестирования формы для добавления студента и документов
    """

    def test_person_form_label(self):
        """
        Функция для тестирования label для поля fio в форме
        """
        form = PersonForm()
        self.assertTrue(form.fields['fio'].label == '*ФИО')

    def test_image_form_help_text(self):
        """
        Функция для тестирования help_text для поля docfile в форме
        """
        form = ImageForm()
        self.assertEqual(form.fields['docfile'].help_text, 'max. 42 megabytes')


class IndexViewTest(TestCase):
    """
    Класс для тестирования отображения
    """

    @classmethod
    def setUpTestData(cls):
        """
        Функция создаёт 10 новых студентов и добавляет их в БД
        """
        college = College.objects.create(title='KKMT')
        specialty = Specialty.objects.create(title='11.11.11 Программирование', college=college)
        group = Group.objects.create(title="П1-17", specialty=specialty)

        number_of_students = 10
        for student_num in range(number_of_students):
            Job.objects.create(fio=f'Иванов Иван Иванович {student_num}', release_year='01.01.2015',
                               employment='Уход в армию', specialty=group, practice_one='РКК Энергия',
                               practice_two='РКК Энергия', budget='Бюджет', phone_number='11111111111',
                               email='foo@example.com')

    def test_view_login(self):
        """
        Функция проверяет отклик страницы /accounts/login/
        """
        c = Client()
        resp = c.post('/accounts/login/', {'username': 'kkmt', 'password': 'kkmtkkmtkkmt'})
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        """
        Функция проверяет отклик страницы /students_base/
        """
        resp = self.client.get('/students_base/')
        self.assertEqual(resp.status_code, 302)  # Код 302 т.к. там идёт redirect

    def test_view_url_accessible_by_name(self):
        """
        Функция проверяет отклик страницы /students_base/ по имени index
        """
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 302) # Код 302 т.к. там идёт redirect

