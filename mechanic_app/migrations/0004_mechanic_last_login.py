# Generated by Django 5.0.7 on 2024-09-23 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic_app', '0003_remove_mechanic_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]