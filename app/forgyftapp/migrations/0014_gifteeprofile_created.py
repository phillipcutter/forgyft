# Generated by Django 2.1.2 on 2018-12-09 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0013_auto_20181202_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='gifteeprofile',
            name='created',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
