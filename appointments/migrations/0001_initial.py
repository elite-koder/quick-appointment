# Generated by Django 4.2.5 on 2023-09-22 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('SHOWED_UP', 'Showed Up'), ('NOT_SHOWED_UP', 'Not Showed Up'), ('CANCELLED', 'Cancelled'), ('DELETED', 'Deleted')], default='SCHEDULED', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]