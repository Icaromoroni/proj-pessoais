from django import forms
from .models import Agendamento

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limitar as opções de seleção para o campo 'nome' aos usuários com cargo 'Cliente'
        self.fields['cliente'].queryset = self.fields['cliente'].queryset.filter(cargo='Cliente', is_staff=False)

