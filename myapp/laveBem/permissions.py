from rest_framework.permissions import BasePermission

class AtendimentoPermission(BasePermission):
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