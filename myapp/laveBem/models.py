from django.db import models
from django.contrib.auth.models import AbstractUser


class Servico(models.Model):
    descricao = models.CharField(max_length=300)
    valor = models.DecimalField(max_digits=8, decimal_places=2, help_text= 'em R$')
    ativo = models.BooleanField(verbose_name='Ativo?', default=True)

    class Meta:
        verbose_name_plural = 'Serviços'
    
    def __str__(self) -> str:
        return self.descricao


class Usuario(AbstractUser):
    CARGO = [
        ('Gerente', 'Gerente'),
        ('Atendente', 'Atendente'),
        ('Helper', 'Helper'),
        ('Cliente', 'Cliente'),
    ]

    cargo = models.CharField(max_length=30, default='Cliente', choices=CARGO)
    funcionario = models.BooleanField(verbose_name='Funcionário?', default=False)
    
    class Meta:
        verbose_name_plural = 'Usuários'
    
    def __str__(self) -> str:
        return self.username


class Agendamento(models.Model):
    cliente_id = models.ForeignKey(Usuario, related_name='agendamentos', on_delete=models.CASCADE, verbose_name='Nome do cliente')
    telefone = models.CharField(max_length=15, help_text='Exemplo: (99) 99999-9999.')
    endereco = models.CharField(max_length=300)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='solicitacoes', verbose_name='Serviço')
    data = models.DateTimeField(help_text='Data de agendamento do serviço.')
    processado = models.BooleanField(verbose_name='Processado?', default=False)
    cancelar = models.BooleanField(verbose_name='Cancelar?', default=False)

    def __str__(self) -> str:
        return self.cliente_id.username


class Atendimento(models.Model):
    SITUACAO = [('Pendente', 'Pendente'),
                ('Realizado', 'Realizado'),
                ('Cancelado', 'Cancelado'),]
    
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='atendimentos')
    situacao = models.CharField(max_length=9, default='Pendente', choices=SITUACAO)
    atendente = models.ForeignKey(Usuario,
                                  on_delete=models.CASCADE,
                                  related_name='atendimentos_atendidos',
                                  limit_choices_to={'cargo': 'Atendente'})
    helper = models.ForeignKey(Usuario,
                               on_delete=models.CASCADE,
                               related_name='atendimentos_ajudados',
                               limit_choices_to={'cargo': 'Helper'})
    data_atendimento = models.DateTimeField(auto_now=True,help_text='Data do atendimento')

class Venda(models.Model):
    PAG = [
        ('1', 'Pix'),
        ('2', 'Debito'),
        ('3', 'Crédito'),
    ]
    atendimento = models.OneToOneField(Agendamento, on_delete=models.CASCADE, related_name='vendas')
    forma_pag = models.CharField(max_length=10, choices=PAG)
    desconto = models.IntegerField(default=0)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, help_text= 'em R$')
    gerente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='desconto', null=True, blank=True)

