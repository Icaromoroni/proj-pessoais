from rest_framework import serializers
from .models import Atendimento, Servico, Agendamento, Usuario
from django.contrib.auth.models import Group


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
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.cargo = validated_data.get('cargo', instance.cargo)
        instance.set_password(validated_data.get('password', instance.password))

        instance.save()
        return instance


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

    def create(self, validated_data):

        usuario, created = Usuario.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.set_password(validated_data.get('password', instance.password))

        instance.save()
        return instance


class ServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        fields = '__all__'


class AgendamentoSerializer(serializers.ModelSerializer):

    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(funcionario=False, is_staff=False), required=False)
    nome_cliente = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AgendamentoSerializer, self).__init__(*args, **kwargs)

        # Define os campos desejados como somente leitura
        campos_proibidos = ['id', 'processado']

        if not self.context['request'].user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            for campo_proibido in campos_proibidos:
                self.fields[campo_proibido].read_only = True

    
    def get_nome_cliente(self, obj):
        return obj.cliente_id.username if obj.cliente_id else None
    
    def get_email(self, obj):
        return obj.cliente_id.email if obj.cliente_id else None

class AtendimentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = '__all__'
        read_only_fields = ['atendente']

    def validate_agendamento(self, value):
        if self.context['request'].method == 'POST' and value.processado:
            raise serializers.ValidationError({'detail': "O atendimento para esse agendamento já foi realizado."})
        return value


    def validate_atendente(self, value):
        # Verifica se o atendente tem o cargo 'Atendente'
        if value.cargo != 'Atendente':
            raise serializers.ValidationError({'detail':"Valor inválido, só é possível adicionar atendentes."})
        return value

    def validate_helper(self, value):
        # Verifica se o helper tem o cargo 'Helper'
        if value.cargo != 'Helper':
            raise serializers.ValidationError({'detail':"Valor inválido, só é possível adicionar helpers."})
        return value


class AgendamentoListSerializer(serializers.ModelSerializer):
    nome_cliente = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        exclude = []
    
    def get_nome_cliente(self, obj):
        return obj.cliente_id.username if obj.cliente_id else None


class AtendimentoListSerializer(serializers.ModelSerializer):

    agendamento = AgendamentoListSerializer(read_only=True)
    nome_atendente = serializers.SerializerMethodField()
    nome_helper = serializers.SerializerMethodField()

    class Meta:
        model = Atendimento
        exclude = []
    
    def get_nome_atendente(self, obj):
        return obj.atendente.username if obj.atendente else None
    
    def get_nome_helper(self, obj):
        return obj.helper.username if obj.helper else None