# Generated by Django 5.2 on 2025-06-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weekly_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklylog',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]
