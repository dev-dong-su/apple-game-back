# Generated by Django 4.2 on 2023-04-05 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apple_game', '0005_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-best_score']},
        ),
    ]