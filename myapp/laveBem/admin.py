from django.contrib import admin
from .models import Agendamento, Usuario, Atendimento
from .forms import AgendamentoForm


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    form = AgendamentoForm


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    pass
