# Generated by Django 2.1.2 on 2018-11-10 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0004_giftidea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftidea',
            name='link',
            field=models.URLField(max_length=600),
        ),
    ]
