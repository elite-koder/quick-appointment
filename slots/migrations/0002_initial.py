# Generated by Django 4.2.5 on 2023-09-22 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('slots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='slots', to=settings.AUTH_USER_MODEL),
        ),
    ]
