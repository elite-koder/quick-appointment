# Generated by Django 4.2.5 on 2023-09-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='slot',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
