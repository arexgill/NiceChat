# Generated by Django 4.2.8 on 2023-12-14 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_userprofile_llm_endpoint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='description',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='receiver_name',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='sender_name',
            new_name='sender',
        ),
    ]
