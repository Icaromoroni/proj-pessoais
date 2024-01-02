from rest_framework import serializers
from .models import Atendimento, Servico, Agendamento, Usuario


class ServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        fields = '__all__'


class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'cargo']
    
    def create(self, validated_data):
        usuario = Usuario.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            cargo = validated_data['cargo']
        )
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario


class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = '__all__'

    def validate_atendente(self, value):
        # Verifica se o atendente tem o cargo 'Atendente'
        if value.cargo != '2':
            raise serializers.ValidationError("O atendente deve ter o cargo 'Atendente'.")
        return value

    def validate_helper(self, value):
        # Verifica se o helper tem o cargo 'Helper'
        if value.cargo != '3':
            raise serializers.ValidationError("O helper deve ter o cargo 'Helper'.")
        return value
    
