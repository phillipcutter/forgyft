# Generated by Django 2.1.2 on 2018-11-17 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0001_squashed_0010_remove_gifteeprofile_fulfilled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifteeprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
