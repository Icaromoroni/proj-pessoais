# Generated by Django 5.0 on 2024-01-02 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laveBem', '0003_alter_atendimento_atendente_alter_atendimento_helper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendimento',
            name='situacao',
            field=models.CharField(choices=[('1', 'Pendente'), ('2', 'Realizado'), ('3', 'Cancelado')], default='Cliente', max_length=9),
        ),
    ]