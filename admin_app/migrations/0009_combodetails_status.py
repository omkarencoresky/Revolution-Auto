# Generated by Django 5.0.7 on 2024-12-09 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0008_combodetails_discount_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='combodetails',
            name='status',
            field=models.CharField(blank=True, default='true', null=True),
        ),
    ]
