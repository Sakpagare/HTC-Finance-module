# Generated by Django 3.2.6 on 2023-07-25 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank_details',
            old_name='acc_no',
            new_name='bank_acc_no',
        ),
        migrations.AddField(
            model_name='bank_details',
            name='bank_name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bank_details',
            name='re_enter_account_no',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='profile_picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blank_cheque', models.ImageField(upload_to='')),
                ('name', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
