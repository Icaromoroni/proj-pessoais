# Generated by Django 5.0 on 2024-01-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laveBem', '0004_alter_atendimento_situacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='funcionario',
            field=models.BooleanField(default=False, verbose_name='Funcionário?'),
        ),
    ]
