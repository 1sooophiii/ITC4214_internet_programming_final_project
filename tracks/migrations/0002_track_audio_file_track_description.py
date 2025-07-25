# Generated by Django 5.2.3 on 2025-07-20 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='tracks/audio/'),
        ),
        migrations.AddField(
            model_name='track',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
