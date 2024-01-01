from django.contrib import admin
from .models import Solicitacao


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ['pessoa','servico','agendamento']
