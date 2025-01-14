# Generated by Django 4.2.8 on 2023-12-21 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_alter_botpersonality_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='botpersonality',
            name='context_length',
            field=models.IntegerField(default=2048, help_text='The number of characters of conversation history to consider for each prompt.'),
        ),
        migrations.AddField(
            model_name='botpersonality',
            name='keywords',
            field=models.TextField(blank=True, help_text='Key topics or words associated with this personality.'),
        ),
        migrations.AddField(
            model_name='botpersonality',
            name='prompt_examples',
            field=models.TextField(blank=True, help_text='Examples of effective prompts for this personality.'),
        ),
        migrations.AddField(
            model_name='botpersonality',
            name='prompt_instruction',
            field=models.TextField(blank=True, help_text='Instructions for crafting prompts for this personality.'),
        ),
        migrations.AddField(
            model_name='botpersonality',
            name='prompt_output_details',
            field=models.TextField(blank=True, help_text='Details on what the output should look like for this personality.'),
        ),
        migrations.AddField(
            model_name='botpersonality',
            name='tone',
            field=models.CharField(blank=True, help_text="The desired tone for this personality's responses.", max_length=250),
        ),
    ]
