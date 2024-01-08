from .models import Servico, Agendamento, Usuario
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404
from django.contrib.auth.hashers import make_password
from .permissions import *


class ServicoListCreate(generics.ListCreateAPIView):

    permission_classes = [AnonimousGerentePermission]

    serializer_class = ServicoSerializer
    queryset = Servico.objects.all()


class ServicoDetailUpdate(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a servico instance.
    """
    permission_classes = [IsAuthenticated, AnonimousGerentePermission]

    serializer_class = ServicoSerializer
    queryset = Servico.objects.all()


class AgendamentoListCreate(generics.ListCreateAPIView):
    """
    List all cliente, or create a new cliente.
    """
    permission_classes = [IsAuthenticated, GerenteAtendetePermission]

    serializer_class = AgendamentoSerializer
    queryset = Agendamento.objects.all()


class AgendamentoDetailUpdate(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a agendamento instance.
    """
    permission_classes = [IsAuthenticated, GerenteAtendetePermission]

    serializer_class = AgendamentoSerializer
    queryset = Agendamento.objects.all()


class BuscarAgendamentoList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, GerenteAtendetePermission]

    serializer_class = AgendamentoSerializer
    # criar classe de filtragem
    def get_queryset(self):

        queryset = Agendamento.objects.all()

        processado = self.request.query_params.get('processado')
        data = self.request.query_params.get('data')
        email = self.request.query_params.get('email')
        pk_servico = self.request.query_params.get('cod')

        if processado:
            queryset = queryset.filter(processado=processado)
        elif data:
            queryset = queryset.filter(data=data)
        elif email:
            queryset = queryset.filter(cliente_id__email=email)
        elif pk_servico:
            queryset = queryset.filter(servico__pk=pk_servico)
        return queryset


class AutoAgendamentoCreate(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def perform_create(self, serializer):
        serializer.save(cliente_id=self.request.user)


class BuscarAutoAgendamentoList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AgendamentoSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = get_list_or_404(Agendamento, cliente_id=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BuscarMeusAgendamentosDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AgendamentoSerializer
    def get_queryset(self):
        return Agendamento.objects.filter(cliente_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(cliente_id=self.request.user)


class FuncionarioListCreate(generics.ListCreateAPIView):
    """
    List all funcionários, or create a new funcionário.
    """
    permission_classes = [IsAuthenticated, GerentePermission]

    serializer_class = UsuarioSerializer

    def list(self, request, *args, **kwargs):
        queryset = get_list_or_404(Usuario, funcionario=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        cargo = data.get('cargo')

        if cargo == 'Cliente':
            raise serializers.ValidationError({'detail': 'Cargo inválido, as opções são "Gerente", "Atendente" e "Helper."'})

        group, created = Group.objects.get_or_create(name=cargo)
        data['groups'] = [group.id]

        data['funcionario'] = True

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        password = self.request.data.get('password')

        hashed_password = make_password(password)

        serializer.validated_data['password'] = hashed_password

        serializer.save()



class FuncionarioDetailUpdate(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a funcionários instance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.groups.filter(name='Gerente').exists():
            return Usuario.objects.filter(funcionario=True)
        elif user.funcionario:
            return Usuario.objects.filter(pk=user.pk, funcionario=True)
        else:
            return Usuario.objects.none()

    def perform_update(self, serializer):
        user = self.request.user

        if not user.is_staff and not user.groups.filter(name='Gerente').exists():
            if user.pk != serializer.instance.pk:
                self.permission_denied(self.request)
        
        novo_cargo = serializer.validated_data.get('cargo', None)

        if novo_cargo:
            instancia = serializer.instance
            grupos_antigos = Group.objects.filter(user=instancia)
            instancia.groups.remove(*grupos_antigos)

            novo_grupo = Group.objects.get(name=novo_cargo)
            instancia.groups.add(novo_grupo)

        password = self.request.data.get('password', None)
        
        if password is not None:
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

        serializer.save()


class ClienteCreate(generics.CreateAPIView):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

    def perform_create(self, serializer):
        password = self.request.data.get('password')

        hashed_password = make_password(password)

        serializer.validated_data['password'] = hashed_password

        serializer.save()

class ClienteList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, GerenteAtendetePermission]
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.filter(funcionario=False, is_staff=False, cargo='Cliente')
    

class ClienteDetailUpdate(generics.RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a clientes instance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            return Usuario.objects.filter(funcionario=False, is_staff=False, cargo='Cliente')
        elif not user.funcionario:
            return Usuario.objects.filter(pk=user.pk, funcionario=False, is_staff=False, cargo='Cliente')
        else:
            return Usuario.objects.none()

    def perform_update(self, serializer):
        user = self.request.user

        if not user.is_staff and not user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            if user.pk != serializer.instance.pk:
                self.permission_denied(self.request)

        password = self.request.data.get('password', None)
        
        if password is not None:
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password

        serializer.save()


class AtendimentoList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, GerenteAtendenteHelperPermission]

    serializer_class = AtendimentoListSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Atendimento.objects.all()
        
        if user.groups.filter(name='Helper'):
            queryset = Atendimento.objects.filter(helper=user)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AtendimentoCreate(generics.CreateAPIView):

    permission_classes = [IsAuthenticated, GerenteAtendenteHelperPermission]
    
    serializer_class = AtendimentoCreateSerializer
    queryset = Atendimento.objects.all()

    def perform_create(self, serializer):

        serializer.save(atendente=self.request.user)

        agendamento = serializer.validated_data['agendamento']
        agendamento.processado = True
        agendamento.save()

        serializer.save()

class AtendimentoDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, GerenteAtendenteHelperPermission]
    queryset = Atendimento.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AtendimentoListSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return AtendimentoCreateSerializer
    
    def perform_update(self, serializer):
        serializer.save(atendente=self.request.user)


class BuscarAtendimentoList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, GerenteAtendenteHelperPermission]

    serializer_class = AtendimentoListSerializer
    # criar classe de filtragem
    def get_queryset(self):

        queryset = Atendimento.objects.all()

        data = self.request.query_params.get('data')
        confirm = self.request.query_params.get('confirm')

        if data:
            if self.request.user.cargo == 'Helper':
                queryset = queryset.filter(data=data, helper=self.request.user)            
            else:
                queryset = queryset.filter(data=data)
        elif confirm:
            if self.request.user.cargo == 'Helper':
                queryset = queryset.filter(confirm_venda=confirm, helper=self.request.user)
            else:
                queryset = queryset.filter(confirm_venda=confirm)
        return queryset

