# Generated by Django 5.0.7 on 2024-11-25 07:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComboDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.CharField(default=0, max_length=20)),
                ('discount_price', models.CharField(default=0, max_length=20)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'combo_details',
            },
        ),
        migrations.CreateModel(
            name='ComboServiceDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='combo_id', to='admin_app.combodetails')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='combo_service_id', to='admin_app.services')),
                ('service_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='combo_service_category_id', to='admin_app.servicecategory')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='combo_service_Type_id', to='admin_app.servicetype')),
            ],
            options={
                'db_table': 'combo_service_details',
            },
        ),
        migrations.CreateModel(
            name='ComboSubServiceDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_service_option_id', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service_detail_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_detail_id', to='admin_app.comboservicedetails')),
                ('sub_service_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_service_id', to='admin_app.subservice')),
            ],
            options={
                'db_table': 'combo_sub_service_details',
            },
        ),
    ]