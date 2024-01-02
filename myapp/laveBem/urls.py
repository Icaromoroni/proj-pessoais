from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', UsuarioListCreate.as_view()),
    path('usuarios/<int:pk>/', UsuarioDetailUpdate.as_view()),
    path('servicos/', ServicoListCreate.as_view()),
    path('servicos/<int:pk>/', ServicoDetailUpdate.as_view()),
    path('agendamento/', AgendamentoListCreate.as_view()),
    path('agendamento/<int:pk>/', AgendamentoDetailUpdate.as_view()),
]