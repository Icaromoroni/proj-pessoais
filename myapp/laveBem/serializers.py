from rest_framework import serializers
from .models import Atendimento, Servico, Agendamento, Usuario


class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'cargo', 'is_active', 'funcionario']
    
    def __init__(self, *args, **kwargs):
        super(UsuarioSerializer, self).__init__(*args, **kwargs)

        campos_proibidos = ['id', 'cargo', 'is_active', 'funcionario']

        user = self.context['request'].user
        if not user.groups.filter(name='Gerente').exists() and not user.is_staff or user.cargo =='Gerente':
            for campo_proibido in campos_proibidos:
                self.fields[campo_proibido].read_only = True
            if user.cargo =='Gerente':
                self.fields[campos_proibidos[3]].read_only = True

        if self.context['request'].method == 'PUT':
            
            self.fields['password'].required=False
            self.fields['username'].required=False
            self.fields['email'].required=False


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
        read_only_fields = ['processado']

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