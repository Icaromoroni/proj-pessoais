from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('funcionarios/', FuncionarioListCreate.as_view()),
    path('funcionarios/<int:pk>/', FuncionarioDetailUpdate.as_view()),
    path('inscrever-se/', ClienteSignupListCreate.as_view()),
    # path('inscrito/<int:pk>/', ClienteSignupDetailUpdate.as_view()),
    path('servicos/', ServicoListCreate.as_view()),
    path('servicos/<int:pk>/', ServicoDetailUpdate.as_view()),
    path('agendamento/', AgendamentoListCreate.as_view()),
    path('agendamento/<int:pk>/', AgendamentoDetailUpdate.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]