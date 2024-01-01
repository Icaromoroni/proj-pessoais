from django.db import models

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
    

class Cliente(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name='cliente')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='clientes', verbose_name='Serviço solicitado')
    agendamento = models.DateTimeField(help_text='Data de agendamento do serviço.')

    def __str__(self) -> str:
        return self.pessoa.nome

class Funcionario(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name='funcionario')
    senha = models.CharField(max_length=40)
    ativo = models.BooleanField(verbose_name='Ativo?', default=True)
    
    class Meta:
        verbose_name_plural = 'Funcionários'
    
    def __str__(self) -> str:
        return self.pessoa.nome
    

class Atendimento(models.Model):
    SITUACAO = [('1', 'Pendente'),
                ('2', 'Realizado'),
                ('3', 'Cancelado'),]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='atendimentos')
    atendente = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='atendimentos_atendidos')
    helper = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='atendimentos_ajudados')
    data_atendimento = models.DateTimeField(help_text='Data do atendimento')
    agendamento = models.DateTimeField(help_text='Data de agendamento do serviço.')
    situacao = models.CharField(max_length=9, default='1', choices=SITUACAO)

    def add(self, pk_atendente, pk_helper):
        self.id_atendente = pk_atendente
        self.id_helper = pk_helper
        self.save()

