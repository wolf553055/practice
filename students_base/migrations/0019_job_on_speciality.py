# Generated by Django 3.0.2 on 2020-02-16 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0018_auto_20200216_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='on_speciality',
            field=models.CharField(blank=True, choices=[('По специальности', 'По специальности'), ('Не по специальности', 'Не по специальности')], max_length=100, null=True),
        ),
    ]