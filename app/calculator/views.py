from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import UsuarioCreationForm
from .models import Operacao
import operator
import numexpr as ne
import re
import math

# Dicionário de operações básicas para referência (não usado diretamente no cálculo principal)
OPERACOES = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

# View customizada de login usando o template personalizado
class CustomLoginView(LoginView):
    template_name = 'calculator/login.html'

@login_required
def calculadora_view(request):
    """
    View responsável por renderizar a página principal da calculadora.
    Responsável por processar as expressões enviadas pelo formulário e
    salvá-las no histórico de cálculos do usuário logado.
    
    Se a expressão for válida, salva no histórico e devolve resultado.
    Caso contrário, exibe mensagem de erro e "Erro" como resultado.
    
    Também carrega o histórico de cálculos do usuário logado e o passa
    como contexto para a template de calculadora.
    """
    expressao = request.POST.get("expressao") if request.method == "POST" else None
    resultado = None
    historico = []
    mensagem = None

    if expressao:
        try:
            # 1) Caso puro de MÓDULO (ex: "4%2" → 4 % 2)
            match_mod = re.fullmatch(r'\s*(\d+)\s*%\s*(\d+)\s*', expressao)
            if match_mod:
                n, m = int(match_mod.group(1)), int(match_mod.group(2))
                resultado = n % m
                Operacao.objects.create(
                    usuario=request.user,
                    numero1=n,
                    numero2=m,
                    operacao='%',
                    resultado=resultado
                )

            else:
                # 2) EXPRESSÃO DE PORCENTAGEM (ex: "45%*5")
                # Transformamos "45%*5" → "0.45*5"
                match_pct = re.fullmatch(r'\s*(\d+(\.\d+)?)%\s*\*\s*(\d+(\.\d+)?)\s*', expressao)
                if match_pct:
                    # extraímos os números
                    raw1, raw2 = float(match_pct.group(1)), float(match_pct.group(3))
                    num1 = raw1 / 100
                    num2 = raw2
                    resultado = num1 * num2
                    Operacao.objects.create(
                        usuario=request.user,
                        numero1=num1,
                        numero2=num2,
                        operacao='*',
                        resultado=resultado
                    )

                else:
                    # 3) QUALQUER OUTRA EXPRESSÃO: avaliamos com numexpr
                    #   - substituir % simples (caso haja) por (/100), mas aqui já tratamos %
                    expressao_proc = expressao

                    # Conta operadores e verifica parênteses
                    operadores = re.findall(r'[\+\-\*/]', expressao_proc)
                    tem_paren = '(' in expressao_proc or ')' in expressao_proc

                    # Avalia resultado
                    resultado = ne.evaluate(expressao_proc).item()

                    # Se for operação simples (1 operador e sem parênteses), salva
                    if len(operadores) == 1 and not tem_paren:
                        op = operadores[0]
                        a, b = expressao.split(op)
                        num1 = ne.evaluate(a).item()
                        num2 = ne.evaluate(b).item()
                        Operacao.objects.create(
                            usuario=request.user,
                            numero1=num1,
                            numero2=num2,
                            operacao=op,
                            resultado=resultado
                        )
                    else:
                        mensagem = (
                            "Expressão complexa (vários operadores ou parênteses) "
                            "não foi salva no histórico."
                        )

        except Exception:
            resultado = "Erro"
            mensagem = "Erro ao processar a expressão."

    # Carrega histórico para exibir
    historico = Operacao.objects.filter(usuario=request.user).order_by("-criado_em")

    return render(request, "calculator/calculadora.html", {
        "resultado": resultado,
        "historico": historico,
        "mensagem": mensagem,
    })

# View para limpar o histórico do usuário logado
@login_required
@require_POST
def limpar_historico(request):
    # Apaga todas as operações do usuário logado
    Operacao.objects.filter(usuario=request.user).delete()
    return redirect('calculadora')

# View de cadastro de novo usuário
def cadastro_view(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            # Salva o novo usuário e faz login automático
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('calculadora')
    else:
        form = UsuarioCreationForm()
    # Renderiza o template de cadastro com o formulário
    return render(request, "calculator/cadastro.html", {"form": form})