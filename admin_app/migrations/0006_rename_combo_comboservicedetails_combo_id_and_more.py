# Generated by Django 5.0.7 on 2024-12-09 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0005_combodetails_usage_limit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comboservicedetails',
            old_name='combo',
            new_name='combo_id',
        ),
        migrations.RenameField(
            model_name='comboservicedetails',
            old_name='service_category',
            new_name='service_category_id',
        ),
        migrations.RenameField(
            model_name='comboservicedetails',
            old_name='service',
            new_name='service_id',
        ),
        migrations.RenameField(
            model_name='comboservicedetails',
            old_name='service_type',
            new_name='service_type_id',
        ),
    ]
