# Generated by Django 4.2 on 2023-04-05 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apple_game', '0004_alter_user_options_delete_score'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
