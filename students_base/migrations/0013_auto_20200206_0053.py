# Generated by Django 3.0.2 on 2020-02-05 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_base', '0012_auto_20200206_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]