# Generated by Django 3.0.2 on 2020-02-25 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0023_auto_20200220_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='list_of_employment',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
