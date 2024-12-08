# Generated by Django 5.1 on 2024-11-27 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsecode',
            name='image_url',
        ),
        migrations.AddField(
            model_name='responsecode',
            name='image_jpg',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='responsecode',
            name='image_webp',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='responsecode',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
