from rest_framework import serializers
from .models import Servico, Pessoa, Solicitacao, Funcionario


class ServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        fields = '__all__'

class PessoaSerializer(serializers.ModelSerializer):

     class Meta:
        model = Pessoa
        fields = '__all__'

class SolicitacaoSerializer(serializers.ModelSerializer):

    pessoa = PessoaSerializer()

    class Meta:
        model = Solicitacao
        fields = '__all__'
    
    def create(self, validated_data):
        pessoa_data = validated_data.pop('pessoa')
        pessoa_instance = Pessoa.objects.create(**pessoa_data)
        cliente_instance = Solicitacao.objects.create(pessoa=pessoa_instance, **validated_data)
        return cliente_instance

    def update(self, instance, validated_data):
        pessoa_data = validated_data.pop('pessoa')
        pessoa_instance = instance.pessoa

        # Atualiza os campos da Pessoa
        pessoa_instance.nome = pessoa_data.get('nome', pessoa_instance.nome)
        pessoa_instance.telefone = pessoa_data.get('telefone', pessoa_instance.telefone)
        pessoa_instance.endereco = pessoa_data.get('endereco', pessoa_instance.endereco)
        pessoa_instance.save()

        # Atualiza os campos do Cliente
        instance.servico = validated_data.get('servico', instance.servico)
        instance.agendamento = validated_data.get('agendamento', instance.agendamento)
        instance.save()

        return instance

class FuncionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Funcionario
        fields = '__all__'
    
    def create(self, validated_data):
        pessoa_data = validated_data.pop('pessoa')
        pessoa_instance = Pessoa.objects.create(**pessoa_data)
        cliente_instance = Funcionario.objects.create(pessoa=pessoa_instance, **validated_data)
        return cliente_instance
    
    def update(self, instance, validated_data):
        pessoa_data = validated_data.pop('pessoa')
        pessoa_instance = instance.pessoa

        # Atualiza os campos da Pessoa
        pessoa_instance.nome = pessoa_data.get('nome', pessoa_instance.nome)
        pessoa_instance.telefone = pessoa_data.get('telefone', pessoa_instance.telefone)
        pessoa_instance.endereco = pessoa_data.get('endereco', pessoa_instance.endereco)
        pessoa_instance.save()

        # Atualiza os campos do Cliente
        instance.servico = validated_data.get('servico', instance.servico)
        instance.agendamento = validated_data.get('agendamento', instance.agendamento)
        instance.save()

        return instance