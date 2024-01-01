from django.urls import path
from .views import ServicoListCreate, ServicoDetailUpdate, SolicitacaoListCreate, SolicitacaoDetailUpdate

urlpatterns = [
    path('servicos/', ServicoListCreate.as_view()),
    path('servicos/<int:pk>/', ServicoDetailUpdate.as_view()),
    path('agendamento/', SolicitacaoListCreate.as_view()),
    path('agendamento/<int:pk>/', SolicitacaoDetailUpdate.as_view()),
]