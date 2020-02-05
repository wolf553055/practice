from django.db import models

IS_BUDGET = (
    ('Бюджет', 'Бюджет'),
    ('Платник', 'Платник')
)

IS_FREE = (
    ('Свободна', 'Свободна'),
    ('Занята', 'Занята')
)


class Job(models.Model):
    fio = models.CharField(max_length=100)
    release_year = models.CharField(max_length=10)
    employment = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    practice_one = models.CharField(max_length=100)
    practice_two = models.CharField(max_length=100)
    budget = models.CharField(max_length=100, choices=IS_BUDGET, default='Бюджет')
    vacancy_st = models.CharField(max_length=100)
    notifications = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=254, help_text='foo@example.com')

    def __str__(self):
        return self.fio


class DocumentImg(models.Model):
    title = models.CharField(max_length=100)
    document = models.ImageField(upload_to='documents/%Y/%m/%d')
    worker = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)


class List_of_employment(models.Model):
    employment = models.CharField(max_length=100)

    def __str__(self):
        return self.employment


class Organization(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    worker = models.OneToOneField(Job, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Skills_Vacancy(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Skills_Student(models.Model):
    fio = models.ForeignKey(Job, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Calls(models.Model):
    fio = models.ForeignKey(Job, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True)
    call_time = models.DateTimeField()
    comment = models.CharField(max_length=150, help_text='max 150 symbols')
    status = models.CharField(max_length=15, null=True, blank=True)
