from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Servico(models.Model):
    descricao = models.CharField(max_length=300)
    valor = models.DecimalField(max_digits=8, decimal_places=2, help_text= 'em R$')
    ativo = models.BooleanField(verbose_name='Ativo?', default=True)

    class Meta:
        verbose_name_plural = 'Serviços'
    
    def __str__(self) -> str:
        return self.descricao

class Agendamento(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome do cliente')
    telefone = models.CharField(max_length=15, help_text='Exemplo: (99) 99999-9999.')
    endereco = models.CharField(max_length=300)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='solicitacoes', verbose_name='Serviço')
    data = models.DateTimeField(help_text='Data de agendamento do serviço.')
    processado = models.BooleanField(verbose_name='Processado?', default=False)

    def __str__(self) -> str:
        return self.nome

class Usuario(AbstractUser):
    CARGO = [
        ('1', 'Gerente'),
        ('2', 'Atendente'),
        ('3', 'Helper'),
        ('4', 'Cliente'),
    ]

    cargo = models.CharField(max_length=30, default='4', choices=CARGO)
    
    class Meta:
        verbose_name_plural = 'Usuários'
    
    def __str__(self) -> str:
        return self.username
 

class Atendimento(models.Model):
    SITUACAO = [('1', 'Pendente'),
                ('2', 'Realizado'),
                ('3', 'Cancelado'),]
    
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='atendimentos')
    situacao = models.CharField(max_length=9, default='1', choices=SITUACAO)
    atendente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='atendimentos_atendidos')
    helper = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='atendimentos_ajudados')
    data_atendimento = models.DateTimeField(help_text='Data do atendimento')

class Venda(models.Model):
    PAG = [
        ('1', 'Pix'),
        ('2', 'Debito'),
        ('3', 'Crédito'),
    ]
    forma_pag = models.CharField(max_length=10, choices=PAG)
    desconto = models.IntegerField(default=0)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, help_text= 'em R$')
    gerente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='desconto', null=True, blank=True)

