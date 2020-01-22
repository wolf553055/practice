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

    def __str__(self):
        return self.fio


class List_of_employment(models.Model):
    employment = models.CharField(max_length=100)

    def __str__(self):
        return self.employment


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=IS_FREE, default='Свободна')

    def __str__(self):
        return self.title


class Skills_Vacancy(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
