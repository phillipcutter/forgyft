# Generated by Django 2.1.2 on 2019-01-13 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0023_scraperinterests_interest_objects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scraperinterests',
            name='generated',
        ),
    ]
