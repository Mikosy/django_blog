# Generated by Django 4.2.8 on 2024-01-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_post_latest_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='latest_post',
            field=models.BooleanField(default=False),
        ),
    ]
