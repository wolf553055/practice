# Generated by Django 3.0.2 on 2020-03-02 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0025_documentimg_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentimg',
            name='document',
            field=models.FileField(upload_to='documents/%Y/%m/%d'),
        ),
    ]
