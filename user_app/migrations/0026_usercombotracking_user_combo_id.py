# Generated by Django 5.0.7 on 2024-11-28 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0025_usercombotracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercombotracking',
            name='user_combo_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_combo_id', to='user_app.usercombopackage'),
        ),
    ]
