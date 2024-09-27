# Generated by Django 5.0.7 on 2024-09-20 10:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mechanic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=225, unique=True)),
                ('phone_no', models.CharField(max_length=20)),
                ('status', models.SmallIntegerField(default=1)),
                ('approved', models.SmallIntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('password', models.CharField(max_length=128)),
                ('profile_image', models.ImageField(default=0, upload_to='mechanic_images/')),
            ],
            options={
                'db_table': 'mechanic',
            },
        ),
    ]