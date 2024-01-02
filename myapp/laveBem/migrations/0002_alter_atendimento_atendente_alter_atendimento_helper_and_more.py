# Generated by Django 5.0 on 2024-01-02 01:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laveBem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendimento',
            name='atendente',
            field=models.ForeignKey(limit_choices_to={'cargo': '2'}, on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos_atendidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='atendimento',
            name='helper',
            field=models.ForeignKey(limit_choices_to={'cargo': '3'}, on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos_ajudados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cargo',
            field=models.CharField(choices=[('Gerente', 'Gerente'), ('Atendente', 'Atendente'), ('Helper', 'Helper'), ('Cliente', 'Cliente')], default='4', max_length=30),
        ),
    ]
