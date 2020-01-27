# Generated by Django 3.0.2 on 2020-01-27 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0007_auto_20200127_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentimg',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documentimg',
            name='document',
            field=models.ImageField(upload_to='documents/%Y/%m/%d'),
        ),
    ]
