# Generated by Django 5.2 on 2025-06-12 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weekly_logs', '0003_alter_weeklylog_week_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklylog',
            name='comment',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
