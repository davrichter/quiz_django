# Generated by Django 4.0.1 on 2022-01-22 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0003_alter_quiz_date created_alter_quiz_dislikes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='Date last edited',
            field=models.DateTimeField(null=True),
        ),
    ]