# Generated by Django 5.0.7 on 2024-11-27 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0021_rename_mechanic_leaves_mechanicleaves_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercombopackage',
            name='car_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='car_Id', to='user_app.usercarrecord'),
            preserve_default=False,
        ),
    ]
