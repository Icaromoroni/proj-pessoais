from .models import Servico, Agendamento, Usuario
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_list_or_404
from .permissions import AtendimentoPermission



class ServicoListCreate(APIView):
    """
    List all servico, or create a new servico.
    """
    def get(self, request, format=None):
        servico = Servico.objects.all()
        serializer = ServicoSerializer(servico, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        user = request.user if type(request.user) != AnonymousUser else None
        
        if not user:
            return Response({'detail': 'As credenciais de autenticação não foram fornecidas.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_staff and not user.groups.filter(name='Gerente').exists():
            return Response({'detail': 'Você não tem permissão para criar um serviço.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ServicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicoDetailUpdate(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Servico.objects.get(pk=pk)
        except Servico.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if not request.user.groups.filter(name='Gerente').exists():
            return Response({'detail': 'Você não tem permissão para visualizar os detalhes do serviço.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        servico = self.get_object(pk)
        serializer = ServicoSerializer(servico)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.user.groups.filter(name='Gerente').exists():
            return Response({'detail': 'Você não tem permissão para atualizar o serviço.'}, status=status.HTTP_401_UNAUTHORIZED)

        servico = self.get_object(pk)
        serializer = ServicoSerializer(servico, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgendamentoListCreate(APIView):
    """
    List all cliente, or create a new cliente.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        if not user.is_staff and not user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            return Response({'detail': 'Você não tem permissão para visualizar todos os agendamentos.'}, status=status.HTTP_401_UNAUTHORIZED)


        cliente = Agendamento.objects.all()
        serializer = AgendamentoSerializer(cliente, many=True, context={'request': request, 'user': user})
        return Response(serializer.data)

    def post(self, request, format=None):
        grupos = ['Gerente', 'Atendente']

        user = request.user

        if not user.is_staff and not user.groups.filter(name__in=grupos).exists():
            return Response({'detail': 'Você não tem permissão para criar um agendamento.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = AgendamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgendamentoDetailUpdate(APIView):
    """
    Retrieve, update or delete a agendamento instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Agendamento.objects.get(pk=pk)
        except Agendamento.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        grupos = ['Gerente', 'Atendente']
        user = request.user
        if not user.is_staff and not request.user.groups.filter(name__in=grupos).exists():
            return Response({'detail': 'Você não tem permissão para concluir a ação.'}, status=status.HTTP_401_UNAUTHORIZED)

        cliente = self.get_object(pk)
        serializer = AgendamentoSerializer(cliente)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        grupos = ['Gerente', 'Atendente']
        user = request.user
        if not user.is_staff and not user.groups.filter(name__in=grupos).exists():
            return Response({'detail': 'Você não tem permissão para concluir a ação.'}, status=status.HTTP_401_UNAUTHORIZED)

        cliente = self.get_object(pk)
        serializer = AgendamentoSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AutoAgendamentoCreate(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]

    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def perform_create(self, serializer):
        serializer.save(cliente_id=self.request.user, processado=False)

class BuscarAgendamentoList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AgendamentoSerializer

    def get_queryset(self):

        queryset = Agendamento.objects.all()

        processado = self.request.query_params.get('p')
        data = self.request.query_params.get('data')
        cliente = self.request.query_params.get('email')
        servico = self.request.query_params.get('cod')

        if processado:
            queryset = queryset.filter(processado=processado)
        elif data:
            queryset = queryset.filter(data=data)
        elif cliente:
            queryset = queryset.filter(cliente_id__email=cliente)
        elif servico:
            queryset = queryset.filter(servico__pk=servico)
        return queryset
    
    def list(self, request, *args, **kwargs):
        grupos = ['Gerente', 'Atendente']
        user = request.user
        queryset = self.get_queryset()

        if not user.is_staff and not user.groups.filter(name__in=grupos).exists():
            return Response({'detail': 'Você não tem permissão para concluir a ação.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BuscarMeusAgendamentosList(generics.ListAPIView):
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

class FuncionarioListCreate(APIView):
    """
    List all funcionários, or create a new funcionário.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        
        user = request.user

        if not user.is_staff and not user.groups.filter(name='Gerente').exists():
            return Response({'detail': 'Você não tem permissão para visualizar funcionários.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        usuario = Usuario.objects.filter(funcionario=True)
        serializer = FuncionarioSerializer(usuario, many=True, context={'request': request, 'user': user})
        return Response(serializer.data)

    def post(self, request, format=None):
                
        user = request.user

        if request.data['cargo'] != 'Cliente':

            if not user.is_staff and not user.groups.filter(name='Gerente').exists():
                return Response({'detail': 'Você não tem permissão para criar um funcionário.'}, status=status.HTTP_401_UNAUTHORIZED)
            request.data['funcionario'] = True

        serializer = FuncionarioSerializer(data=request.data, context={'request': request, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FuncionarioDetailUpdate(APIView):
    """
    Retrieve, update or delete a funcionários instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk, funcionario=True)
        except Usuario.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        
        user = request.user

        if user.is_staff or user.groups.filter(name='Gerente').exists():
            funcionario = self.get_object(pk)
        elif user.pk != pk:
            raise Http404
        else:
            funcionario = self.get_object(user.pk)
        serializer = FuncionarioSerializer(funcionario, context={'request': request, 'user': user})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        
        user = request.user

        if user.is_staff or request.user.groups.filter(name='Gerente').exists():
            funcionario = self.get_object(pk)
        elif user.pk != pk:
            raise Http404
        else:
            funcionario = self.get_object(user.pk)

        serializer = FuncionarioSerializer(funcionario, data=request.data, context={'request': request, 'user': user}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteListCreate(APIView):
    """
    List all clientes, or create a new cliente.
    """
    def get(self, request, format=None):

        user = request.user if type(request.user) != AnonymousUser else None
        
        if not user:
            return Response({'detail': 'As credenciais de autenticação não foram fornecidas.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_staff and not user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            return Response({'detail': 'Permissão negada.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        usuario = Usuario.objects.filter(funcionario=False, is_staff=False)
        serializer = ClienteSerializer(usuario, many=True, context={'request': request, 'user': user})
        return Response(serializer.data)  
 
    def post(self, request, format=None):

        user = request.user

        serializer = ClienteSerializer(data=request.data, context={'request': request, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ClienteDetailUpdate(APIView):
    """
    Retrieve, update or delete a clientes instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk, funcionario=False, is_staff=False)
        except Usuario.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        
        user = request.user

        if user.is_staff or user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            cliente = self.get_object(pk)
        elif user.pk != pk:
            raise Http404
        else:
            cliente = self.get_object(user.pk)

        serializer = ClienteSerializer(cliente, context={'request': request, 'user': user})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        
        user = request.user

        if user.is_staff or request.user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            cliente = self.get_object(pk)
        elif user.pk != pk:
            raise Http404
        else:
            cliente = self.get_object(user.pk)

        serializer = ClienteSerializer(cliente, data=request.data, context={'request': request, 'user': user}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtendimentoList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, AtendimentoPermission]

    serializer_class = AtendimentoListSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = Atendimento.objects.all()
        
        if user.groups.filter(name='Helper'):
            queryset = Atendimento.objects.filter(helper=user)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AtendimentoCreate(generics.CreateAPIView):

    permission_classes = [IsAuthenticated, AtendimentoPermission]
    
    serializer_class = AtendimentoCreateSerializer
    queryset = Atendimento.objects.all()

    def perform_create(self, serializer):

        serializer.save(atendente=self.request.user)

        agendamento = serializer.validated_data['agendamento']
        agendamento.processado = True
        agendamento.save()

        serializer.save()

class AtendimentoDetailUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, AtendimentoPermission]
    queryset = Atendimento.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AtendimentoListSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return AtendimentoCreateSerializer
    
    def perform_update(self, serializer):
        serializer.save(atendente=self.request.user)


