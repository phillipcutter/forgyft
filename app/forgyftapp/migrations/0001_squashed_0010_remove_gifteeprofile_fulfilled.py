# Generated by Django 2.1.2 on 2018-11-17 20:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import forgyftapp.models


class Migration(migrations.Migration):

    replaces = [('forgyftapp', '0001_initial'), ('forgyftapp', '0002_gifteeprofile_user'), ('forgyftapp', '0003_gifteeprofile_fulfilled'), ('forgyftapp', '0004_giftidea'), ('forgyftapp', '0005_auto_20181110_2228'), ('forgyftapp', '0006_auto_20181111_0153'), ('forgyftapp', '0007_giftidea_published'), ('forgyftapp', '0008_gifteeprofile_published'), ('forgyftapp', '0009_gifteeprofile_name'), ('forgyftapp', '0010_remove_gifteeprofile_fulfilled')]

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('_slug', models.SlugField(blank=True, max_length=7)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(forgyftapp.models.OnCreate, models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='GifteeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interests', models.TextField()),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fulfilled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GiftIdea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.TextField()),
                ('link', models.URLField(max_length=600)),
                ('giftee_profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ideas', to='forgyftapp.GifteeProfile')),
                ('published', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='age',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='existing_related_items',
            field=models.TextField(default='', max_length=6000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='extra_info',
            field=models.TextField(default='', max_length=6000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='gender',
            field=models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='MALE', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='price_upper',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='relationship',
            field=models.TextField(default='Friend', max_length=6000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gifteeprofile',
            name='interests',
            field=models.TextField(max_length=6000),
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gifteeprofile',
            name='name',
            field=models.TextField(default='bob', max_length=150),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='gifteeprofile',
            name='fulfilled',
        ),
    ]
