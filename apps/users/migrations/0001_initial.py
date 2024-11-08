# Generated by Django 5.1.3 on 2024-11-05 19:49

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('is_active', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid email address.', regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'), django.core.validators.MinLengthValidator(8)], verbose_name='Email address')),
                ('username', models.CharField(blank=True, max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Username can only contain letters, numbers, dots, underscores, and hyphens.', regex='^[a-zA-Z0-9_.-]+$'), django.core.validators.MinLengthValidator(4)], verbose_name='Username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the admin site', verbose_name='staff status')),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.MinLengthValidator(8)], verbose_name='Password')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['created_at'],
            },
        ),
    ]
