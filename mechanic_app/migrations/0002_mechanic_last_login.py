# Generated by Django 5.0.7 on 2024-09-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanic_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]