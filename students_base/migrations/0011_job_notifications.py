# Generated by Django 3.0.2 on 2020-02-04 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0010_calls_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='notifications',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]