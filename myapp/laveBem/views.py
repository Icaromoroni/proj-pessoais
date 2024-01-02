from .models import Servico, Agendamento, Usuario
from .serializers import ServicoSerializer, AgendamentoSerializer, UsuarioSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class ServicoListCreate(APIView):
    """
    List all servico, or create a new servico.
    """
    def get(self, request, format=None):
        servico = Servico.objects.all()
        serializer = ServicoSerializer(servico, many=True)
        return Response(serializer.data)
    
    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):
        if not request.user.groups.filter(name='Gerente').exists():
            return Response({'error': 'Você não tem permissão para criar um serviço.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ServicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicoDetailUpdate(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Servico.objects.get(pk=pk)
        except Servico.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        servico = self.get_object(pk)
        serializer = ServicoSerializer(servico)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def put(self, request, pk, format=None):
        if not request.user.groups.filter(name='Gerente').exists():
            return Response({'error': 'Você não tem permissão para atualizar um serviço.'}, status=status.HTTP_403_FORBIDDEN)

        servico = self.get_object(pk)
        serializer = ServicoSerializer(servico, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     servico = self.get_object(pk)
    #     servico.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class AgendamentoListCreate(APIView):
    """
    List all cliente, or create a new cliente.
    """
    def get(self, request, format=None):
        cliente = Agendamento.objects.all()
        serializer = AgendamentoSerializer(cliente, many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):

        serializer = AgendamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class AgendamentoDetailUpdate(APIView):
    """
    Retrieve, update or delete a agendamento instance.
    """
    def get_object(self, pk):
        try:
            return Agendamento.objects.get(pk=pk)
        except Agendamento.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cliente = self.get_object(pk)
        serializer = AgendamentoSerializer(cliente)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        cliente = self.get_object(pk)
        serializer = AgendamentoSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @permission_classes([IsAuthenticated])
class UsuarioListCreate(APIView):
    """
    List all servico, or create a new servico.
    """
    def get(self, request, format=None):
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data)
    
    @permission_classes([IsAuthenticated])
    def post(self, request, format=None):
        # if not request.user.groups.filter(name='Gerente').exists():
        #     return Response({'error': 'Você não tem permissão para criar um serviço.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

