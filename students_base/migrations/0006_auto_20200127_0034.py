# Generated by Django 3.0.2 on 2020-01-27 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0005_documentimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentimg',
            name='document',
            field=models.ImageField(upload_to='media/'),
        ),
    ]