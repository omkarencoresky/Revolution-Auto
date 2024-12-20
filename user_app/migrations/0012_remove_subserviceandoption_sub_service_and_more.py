# Generated by Django 5.0.7 on 2024-11-08 06:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0011_alter_bookingandquote_schedule_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subserviceandoption',
            name='sub_service',
        ),
        migrations.RemoveField(
            model_name='subserviceandoption',
            name='sub_service_option',
        ),
        migrations.AddField(
            model_name='subserviceandoption',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2024-10-24 14:57:02.007373+05:30'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subserviceandoption',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='SubServiceBasedOption',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_service', models.CharField(max_length=500)),
                ('sub_service_option', models.CharField(max_length=500)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subServiceAndOptionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subServiceAndOptionId', to='user_app.subserviceandoption')),
            ],
            options={
                'db_table': 'sub_service_based_option',
            },
        ),
    ]
