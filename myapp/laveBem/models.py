from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class Servico(models.Model):
    descricao = models.CharField(max_length=300)
    valor = models.DecimalField(max_digits=8, decimal_places=2, help_text= 'em R$')
    ativo = models.BooleanField(verbose_name='Ativo?', default=True)

    class Meta:
        verbose_name_plural = 'Serviços'
    
    def __str__(self) -> str:
        return self.descricao

class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.nome
    

class Solicitacao(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name='solicitacao')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='solicitacoes', verbose_name='Serviço solicitado')
    agendamento = models.DateTimeField(help_text='Data de agendamento do serviço.')
    processado = models.BooleanField(verbose_name='Processado?', default=False)

    class Meta:
        verbose_name_plural = 'Solicitações'

    def __str__(self) -> str:
        return self.pessoa.nome

class Funcionario(models.Model):

    CARGO = [
        ('1', 'Gerente'),
        ('2', 'Atendente'),
        ('3', 'Helper'),

    ]

    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name='funcionario')
    cargo = models.CharField(max_length=30, choices=CARGO)
    senha = models.CharField(max_length=40)
    ativo = models.BooleanField(verbose_name='Ativo?', default=True)
    
    class Meta:
        verbose_name_plural = 'Funcionários'
    
    def save(self, *args, **kwargs):
        # Ao salvar, se a senha não estiver criptografada, criptografa
        if not self.senha.startswith('bcrypt'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.pessoa.nome
    

class Atendimento(models.Model):
    SITUACAO = [('1', 'Pendente'),
                ('2', 'Realizado'),
                ('3', 'Cancelado'),]
    
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name='atendimentos')
    situacao = models.CharField(max_length=9, default='1', choices=SITUACAO)
    atendente = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='atendimentos_atendidos')
    helper = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='atendimentos_ajudados')
    data_atendimento = models.DateTimeField(help_text='Data do atendimento')

    def add(self, pk_atendente, pk_helper):
        self.id_atendente = pk_atendente
        self.id_helper = pk_helper
        self.save()

