from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class GerenteAtendenteHelperPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        grupos = ['Gerente', 'Atendente']

        if user.is_staff or user.groups.filter(name__in=grupos).exists():
            return True
        elif user.groups.filter(name='Helper').exists():
            return request.method == 'GET'

        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.helper or request.user.is_staff or request.user.groups.filter(name__in=['Gerente', 'Atendente']).exists():
            return True
        return False

class AnonimousGerentePermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user

        if request.method == 'GET':
            return user

        elif request.method == 'POST':
            return user and (user.is_staff or user.groups.filter(name='Gerente').exists())

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        return user and (user.is_staff or user.groups.filter(name='Gerente').exists())
    
class GerenteAtendetePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method == 'GET':
            return user.groups.filter(name__in=['Gerente', 'Atendente']).exists()

        elif request.method == 'POST':
            # Apenas usuários autenticados e com permissão de Gerente ou Atendente podem criar agendamentos
            return user and user.groups.filter(name__in=['Gerente', 'Atendente']).exists()

        return False

    def has_object_permission(self, request, view, obj):
        # Apenas usuários autenticados e com permissão de Gerente ou Atendente podem acessar/modificar agendamentos existentes
        user = request.user
        return user and user.groups.filter(name__in=['Gerente', 'Atendente']).exists()


class GerentePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

        if request.method in methods:
            # Verificar permissões para a listagem de funcionários
            return user.is_staff or user.groups.filter(name='Gerente').exists()

        return False

class VendaPermission(BasePermission):
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)