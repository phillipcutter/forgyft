# Generated by Django 2.1.2 on 2018-12-09 06:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0016_gifteeprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifteeprofile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
