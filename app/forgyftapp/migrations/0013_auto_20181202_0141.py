# Generated by Django 2.1.2 on 2018-12-02 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0012_auto_20181202_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifteeprofile',
            name='extra_info',
            field=models.TextField(blank=True, max_length=6000, null=True),
        ),
    ]