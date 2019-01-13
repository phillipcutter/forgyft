# Generated by Django 2.1.2 on 2019-01-13 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ScrapeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('price', models.FloatField(null=True)),
                ('url', models.URLField()),
                ('image_url', models.URLField(null=True)),
            ],
        ),
    ]
