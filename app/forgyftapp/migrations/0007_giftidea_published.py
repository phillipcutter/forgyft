# Generated by Django 2.1.2 on 2018-11-11 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0006_auto_20181111_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftidea',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]