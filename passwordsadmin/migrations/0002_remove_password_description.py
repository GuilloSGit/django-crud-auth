# Generated by Django 5.1.1 on 2024-10-26 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passwordsadmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='password',
            name='description',
        ),
    ]