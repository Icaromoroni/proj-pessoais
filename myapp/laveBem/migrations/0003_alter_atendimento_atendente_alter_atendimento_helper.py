# Generated by Django 5.0 on 2024-01-02 01:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laveBem', '0002_alter_atendimento_atendente_alter_atendimento_helper_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atendimento',
            name='atendente',
            field=models.ForeignKey(limit_choices_to={'cargo': 'Atendente'}, on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos_atendidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='atendimento',
            name='helper',
            field=models.ForeignKey(limit_choices_to={'cargo': 'Helper'}, on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos_ajudados', to=settings.AUTH_USER_MODEL),
        ),
    ]
