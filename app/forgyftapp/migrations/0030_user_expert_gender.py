# Generated by Django 2.1.2 on 2019-02-03 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forgyftapp', '0029_auto_20190203_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expert_gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='MALE', max_length=80),
            preserve_default=False,
        ),
    ]
