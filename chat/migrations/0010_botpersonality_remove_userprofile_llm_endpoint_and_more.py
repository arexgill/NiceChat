# Generated by Django 4.2.8 on 2023-12-21 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_rename_messages_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotPersonality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('portrait', models.ImageField(null=True, upload_to='images/')),
                ('avatar', models.ImageField(null=True, upload_to='images/')),
                ('predict_prefix', models.CharField(blank=True, max_length=2048)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='llm_endpoint',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='grounding_source',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
