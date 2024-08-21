# Generated by Django 5.0.7 on 2024-08-21 04:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('image_url', models.ImageField(upload_to='media/')),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'car_brand',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=50)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.carbrand')),
            ],
            options={
                'db_table': 'car_model',
            },
        ),
        migrations.CreateModel(
            name='CarYear',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.CharField(max_length=4)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.carbrand')),
            ],
            options={
                'db_table': 'car_year',
            },
        ),
        migrations.CreateModel(
            name='CarTrim',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('car_trim_name', models.CharField(max_length=100)),
                ('status', models.SmallIntegerField(default=1)),
                ('remember_token', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.carbrand')),
                ('model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.carmodel')),
                ('year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.caryear')),
            ],
            options={
                'db_table': 'car_trim',
            },
        ),
        migrations.AddField(
            model_name='carmodel',
            name='year_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.caryear'),
        ),
    ]