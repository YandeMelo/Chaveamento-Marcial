# Generated by Django 5.0 on 2024-01-09 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_teste_BD', '0003_alter_lutador_telefone_alter_mestre_telefone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lutador',
            name='graduacao',
        ),
        migrations.RemoveField(
            model_name='mestre',
            name='graduacao',
        ),
    ]
