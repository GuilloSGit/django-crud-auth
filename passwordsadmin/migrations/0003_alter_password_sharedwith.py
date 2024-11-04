# Generated by Django 5.1.1 on 2024-10-27 01:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passwordsadmin', '0002_remove_password_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='password',
            name='sharedWith',
            field=models.ManyToManyField(blank=True, related_name='shared_passwords', to=settings.AUTH_USER_MODEL),
        ),
    ]
