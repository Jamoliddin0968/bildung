# Generated by Django 5.1.1 on 2024-10-01 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_subject_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='question_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subject',
            name='question_time',
            field=models.IntegerField(default=60),
        ),
    ]
