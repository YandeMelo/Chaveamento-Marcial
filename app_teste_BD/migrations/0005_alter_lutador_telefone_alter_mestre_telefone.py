# Generated by Django 5.0.1 on 2024-01-17 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_teste_BD', '0004_remove_lutador_graduacao_remove_mestre_graduacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lutador',
            name='telefone',
            field=models.IntegerField(help_text='Exemplo: (XX)XXXXX-XXXX / Apenas números', max_length=11),
        ),
        migrations.AlterField(
            model_name='mestre',
            name='telefone',
            field=models.IntegerField(help_text='Exemplo: (XX)XXXXX-XXXX / Apenas números', max_length=11),
        ),
    ]
