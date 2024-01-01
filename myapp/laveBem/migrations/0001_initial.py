# Generated by Django 5.0 on 2024-01-01 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agendamento', models.DateTimeField(help_text='Data de agendamento do serviço.')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('senha', models.CharField(max_length=40)),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
            ],
            options={
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=15)),
                ('endereco', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=300)),
                ('valor', models.DecimalField(decimal_places=2, help_text='em R$', max_digits=8)),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
            ],
            options={
                'verbose_name_plural': 'Serviços',
            },
        ),
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_atendimento', models.DateTimeField(help_text='Data do atendimento')),
                ('agendamento', models.DateTimeField(help_text='Data de agendamento do serviço.')),
                ('situacao', models.CharField(choices=[('1', 'Pendente'), ('2', 'Realizado'), ('3', 'Cancelado')], default='1', max_length=9)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos', to='laveBem.cliente')),
                ('atendente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos_atendidos', to='laveBem.funcionario')),
                ('helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atendimentos_ajudados', to='laveBem.funcionario')),
            ],
        ),
        migrations.AddField(
            model_name='funcionario',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to='laveBem.pessoa'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='laveBem.pessoa'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clientes', to='laveBem.servico', verbose_name='Serviço solicitado'),
        ),
    ]
