# Generated by Django 3.2.6 on 2023-07-26 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20230725_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company_profile',
            name='country',
        ),
    ]
