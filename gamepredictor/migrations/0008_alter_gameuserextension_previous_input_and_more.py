# Generated by Django 4.1.3 on 2023-03-26 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamepredictor', '0007_alter_gameuserextension_previous_input_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameuserextension',
            name='previous_input',
            field=models.ManyToManyField(blank=True, related_name='previous_input', related_query_name='previous_input', to='gamepredictor.games'),
        ),
        migrations.AlterField(
            model_name='gameuserextension',
            name='reported_games',
            field=models.ManyToManyField(blank=True, related_name='reported_games', related_query_name='reported_games', to='gamepredictor.games'),
        ),
    ]
