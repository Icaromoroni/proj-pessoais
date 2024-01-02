from rest_framework import serializers
from .models import Servico, Agendamento, Usuario


class ServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        fields = '__all__'


class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password']
    
