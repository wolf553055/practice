# Generated by Django 3.0.2 on 2020-02-08 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0014_auto_20200208_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialty',
            name='college',
        ),
    ]
