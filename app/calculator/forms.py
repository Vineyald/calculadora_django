from django import forms
from calculator.models import Operacao, Usuario
from django.contrib.auth.forms import UserCreationForm

class CalculadoraForm(forms.Form):
    numero1 = forms.FloatField()
    numero2 = forms.FloatField()
    operacao = forms.ChoiceField(choices=Operacao.OPERACOES)

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("name", "email")

