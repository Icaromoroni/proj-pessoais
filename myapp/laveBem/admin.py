from django.contrib import admin
from .models import Agendamento, Usuario


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['nome','servico','data']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass
