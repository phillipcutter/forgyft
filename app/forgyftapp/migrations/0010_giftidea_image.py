# Generated by Django 2.1.2 on 2018-11-30 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0009_giftidea_clicks'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftidea',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]