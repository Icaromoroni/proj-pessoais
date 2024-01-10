from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('funcionarios/', FuncionarioListCreate.as_view()),
    path('funcionarios/<int:pk>/', FuncionarioDetailUpdate.as_view()),

    path('inscrever-se/', ClienteCreate.as_view()),
    path('inscritos/', ClienteList.as_view()),
    path('inscritos/<int:pk>/', ClienteDetailUpdate.as_view()),

    path('servicos/', ServicoListCreate.as_view()),
    path('servicos/<int:pk>/', ServicoDetailUpdate.as_view()),

    path('agendamentos/', AgendamentoListCreate.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetailUpdate.as_view()),
    path('buscar/agendamentos/', BuscarAgendamentoList.as_view()),

    path('auto-agendamento/', AutoAgendamentoCreate.as_view()),
    path('buscar/meus-agendamentos/', BuscarAutoAgendamentoList.as_view()),
    path('buscar/meus-agendamentos/<int:pk>/', BuscarMeusAgendamentosDetailUpdate.as_view()),
    
    path('atendimentos/', AtendimentoList.as_view()),
    path('atendimentos/<int:pk>/', AtendimentoDetailUpdate.as_view()),
    path('buscar/atendimentos/', BuscarAtendimentoList.as_view()),
    path('cadastro/atendimento/', AtendimentoCreate.as_view()),


    path('venda/', VendaListCreate.as_view()),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]