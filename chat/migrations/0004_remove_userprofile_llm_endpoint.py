# Generated by Django 4.2.8 on 2023-12-13 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_userprofile_is_bot_userprofile_llm_endpoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='llm_endpoint',
        ),
    ]
