# Generated by Django 5.1.5 on 2025-01-24 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
