from rest_framework import serializers
from .models import Atendimento, Servico, Agendamento, Usuario
from django.contrib.auth.models import Group


class ServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        fields = '__all__'


class AgendamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = '__all__'


class FuncionarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'cargo', 'is_active', 'funcionario']
    
    def __init__(self, *args, **kwargs):
        super(FuncionarioSerializer, self).__init__(*args, **kwargs)

        # Define os campos desejados como somente leitura
        campos_proibidos = ['id', 'cargo', 'is_active', 'funcionario']

        if not self.context['request'].user.groups.filter(name__in=['Gerente']).exists() and not self.context['user'].is_staff:
            for campo_proibido in campos_proibidos:
                self.fields[campo_proibido].read_only = True
        if self.context['request'].user.groups.filter(name__in=['Gerente']).exists() and self.context['user'].is_staff:
            self.fields[campos_proibidos[3]].read_only = True

    def create(self, validated_data):
        funcionario_data = validated_data.pop('funcionario', False)
        cargo = validated_data.get('cargo')

        if cargo == 'Cliente':
            raise serializers.ValidationError({'detail':'Cargo inválido, as opções são "Gerente", "Atendente" e "Helper".'})

        usuario, created = Usuario.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
            defaults={'cargo': cargo}
        )

        # Adiciona o usuário ao grupo correspondente ao cargo
        try:
            group = Group.objects.get(name=cargo)
            usuario.groups.add(group)
        except Group.DoesNotExist:
            # Lidere com o caso onde o grupo correspondente ao cargo não existe
            pass

        usuario.funcionario = funcionario_data
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario


class ClienteSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'cargo', 'funcionario']
    
    def __init__(self, *args, **kwargs):
        super(ClienteSerializer, self).__init__(*args, **kwargs)

        # Define os campos desejados como somente leitura
        campos_proibidos = ['id', 'cargo', 'funcionario']

        if not self.context['request'].user.groups.filter(name__in=['Gerente']).exists() and not self.context['user'].is_staff:
            for campo_proibido in campos_proibidos:
                self.fields[campo_proibido].read_only = True
        if self.context['request'].user.groups.filter(name__in=['Gerente']).exists():
            self.fields[campos_proibidos[3]].read_only = True

    def create(self, validated_data):

        usuario, created = Usuario.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
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
            raise serializers.ValidationError({'detail':"O atendente deve ter o cargo 'Atendente'."})
        return value

    def validate_helper(self, value):
        # Verifica se o helper tem o cargo 'Helper'
        if value.cargo != '3':
            raise serializers.ValidationError({'detail':"O helper deve ter o cargo 'Helper'."})
        return value
    
