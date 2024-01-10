from rest_framework import serializers
from .models import Atendimento, Servico, Agendamento, Usuario, Venda
from django.contrib.auth.models import AnonymousUser


class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        exclude = ["is_staff", "user_permissions", "is_superuser"]
    
    def __init__(self, *args, **kwargs):
        super(UsuarioSerializer, self).__init__(*args, **kwargs)

        request = self.context['request']

        campos_proibidos_users = ['id', 'cargo', 'is_active', 'funcionario', 'groups',  "date_joined", "last_login"]
        campos_proibidos_gerente = ['id', 'funcionario', 'groups', "date_joined", "last_login"]

        user = request.user

        if not user.groups.filter(name='Gerente').exists() and not user.is_staff or user.cargo =='Gerente':
            if type(user) != AnonymousUser and user.cargo =='Gerente':
                if request.method == 'PUT':
                    for campo_proibido in campos_proibidos_gerente:
                        self.fields[campo_proibido].read_only = True
            else:
                for campo_proibido in campos_proibidos_users:
                    self.fields[campo_proibido].read_only = True

        if request.method == 'PUT':
            self.fields['password'].required=False
            self.fields['username'].required=False
            self.fields['email'].required=False

class ServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        fields = '__all__'

class ServicoListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Servico
        exclude = ['ativo']


class AgendamentoSerializer(serializers.ModelSerializer):

    cliente = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(funcionario=False, is_staff=False), required=False)
    nome_cliente = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = '__all__'
        read_only_fields = ['processado']

    def get_nome_cliente(self, obj):
        return obj.cliente.username if obj.cliente else None
    
    def get_email(self, obj):
        return obj.cliente.email if obj.cliente else None


class AgendamentoListSerializer(serializers.ModelSerializer):
    nome_cliente = serializers.SerializerMethodField()
    servico = ServicoListSerializer(read_only=True)

    class Meta:
        model = Agendamento
        exclude = []
    
    def get_nome_cliente(self, obj):
        return obj.cliente.username if obj.cliente else None


class AtendimentoCreateSerializer(serializers.ModelSerializer):

    nome_atendente = serializers.SerializerMethodField()
    nome_helper = serializers.SerializerMethodField()

    class Meta:
        model = Atendimento
        fields = '__all__'
        read_only_fields = ['atendente']

    def get_nome_atendente(self, obj):
        return obj.atendente.username if obj.atendente else None
    
    def get_nome_helper(self, obj):
        return obj.helper.username if obj.helper else None

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


class AtendimentoListSerializer(serializers.ModelSerializer):

    agendamento = AgendamentoListSerializer(read_only=True)
    nome_atendente = serializers.SerializerMethodField()
    nome_helper = serializers.SerializerMethodField()

    class Meta:
        model = Atendimento
        fields = '__all__'
    
    def get_nome_atendente(self, obj):
        return obj.atendente.username if obj.atendente else None
    
    def get_nome_helper(self, obj):
        return obj.helper.username if obj.helper else None

class VendaListSerializer(serializers.ModelSerializer):
    atendimento = AtendimentoListSerializer(read_only=True)

    class Meta:
        model = Venda
        fields = '__all__'

class VendaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venda
        fields = '__all__'