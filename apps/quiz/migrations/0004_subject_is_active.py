# Generated by Django 5.1.1 on 2024-10-05 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]