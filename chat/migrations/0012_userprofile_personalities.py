# Generated by Django 4.2.8 on 2023-12-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_alter_botpersonality_options_alter_friends_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='personalities',
            field=models.ManyToManyField(blank=True, related_name='users', to='chat.botpersonality'),
        ),
    ]
