# Generated by Django 4.2.8 on 2023-12-17 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_rename_messages_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time', models.TimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='stock_answer',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AddField(
            model_name='messages',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='chat.userprofile'),
        ),
        migrations.AddField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='chat.userprofile'),
        ),
    ]
