# Generated by Django 3.0.2 on 2020-01-24 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0004_auto_20200123_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='status',
        ),
    ]
