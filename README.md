# 🧮 Calculadora Avançada Django

Projeto de desafio técnico: uma calculadora web com autenticação de usuários, suporte a expressões matemáticas avançadas e histórico individual de cálculos. Desenvolvido com Django, Docker e Tailwind CSS.

---

## 📑 Sumário

- [Funcionalidades](#-funcionalidades)  
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)  
- [Como Executar](#como-executar)  
  - [Usando Docker (recomendado)](#usando-docker-recomendado)  
  - [Sem Docker (ambiente local)](#sem-docker-ambiente-local)  
- [Como Usar](#️-como-usar)  
- [Lógica Avançada da Calculadora](#-lógica-avançada-da-calculadora)  
- [Estrutura do Projeto](#️-estrutura-do-projeto)  
- [Decisões Técnicas](#-decisões-técnicas)  
- [Observações](#-observações)  
- [Licença](#-licença)

---

## ✨ Funcionalidades

- Cadastro e login de usuários com modelo customizado 🔐  
- Operações matemáticas básicas (+, -, *, /), porcentagem (%) e modulo (%)  
- Histórico individual de cálculos salvos por usuário 🕓  
- Interface moderna e responsiva com Tailwind CSS 🎨  
- Logout com sessão protegida 🚪

---

## 🛠 Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)  
- [Django 5+](https://www.djangoproject.com/)  
- [numexpr](https://numexpr.readthedocs.io/) — execução segura de expressões  
- [Tailwind CSS via CDN](https://tailwindcss.com/)  
- Docker & Docker Compose 🐳  
- SQLite (banco embutido, sem necessidade de configuração)

---

## 🚀 Como executar

### Usando Docker (recomendado)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Vineyald/calculadora_django.git
   cd calculadora_django/app
   ```

2. **Suba o ambiente:**
   ```bash
   docker-compose up --build
   ```

3. **Acesse no navegador:**
   ```
   http://localhost:8000
   ```

---

### Sem Docker (ambiente local)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Vineyald/calculadora_django.git
   cd calculadora_django/app
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

7. **Acesse no navegador:**
   ```
   http://localhost:8000
   ```

---

## ▶️ Como usar

1. **Acesse a aplicação no navegador:**  
   [http://localhost:8000](http://localhost:8000)

2. **Crie um novo usuário:**  
   Clique em **"Cadastre-se"** na tela de login e preencha o formulário de cadastro.  
   > ⚠️ **Atenção:** É obrigatório criar um usuário para acessar e utilizar a calculadora.

3. **Faça login:**  
   Após o cadastro, entre com seu e-mail e senha.

4. **Utilize a calculadora:**  
   - Realize operações matemáticas básicas, porcentagem (%) e use o botão **±** para inverter o sinal do último número digitado.
   - O histórico de cálculos é salvo apenas para o usuário logado.

5. **Logout:**  
   Clique em **"Sair"** para encerrar sua sessão com segurança.

---   

## 🧠 Lógica Avançada da Calculadora

A aplicação interpreta expressões conforme regras específicas:

| Expressão    | Interpretação              | Histórico | Mensagem                         |
|--------------|----------------------------|-----------|----------------------------------|
| `45+5`       | Soma simples               | ✔️ Salva   | —                                |
| `45%*5`      | Porcentagem: 45% × 5       | ✔️ Salva   | —                                |
| `4%2`        | Modulo: 4%2 = 0          | ✔️ Salva   | —                                |
| `45+5*2`     | Expressão complexa         | ❌ Não salva | Exibe aviso no frontend         |
| `4*(5+3)`    | Uso de parênteses          | ❌ Não salva | Exibe aviso no frontend         |
| Expressão inválida | Erro de sintaxe ou cálculo | ❌ Não salva | Resultado “Erro” e aviso        |

> ⚠️ Quando a expressão **não é salva**, informamos com uma mensagem no topo da página:
> **"Expressão complexa não salva no histórico."**

---

## 🔧 Decisões Técnicas

- **Modelo de usuário customizado**: Utiliza `calculator.Usuario`, baseado em `AbstractBaseUser`, permitindo login por e-mail
- **Execução das expressões**: Utiliza a biblioteca `numexpr`, mais segura do que `eval`
- **Identificação das expressões**: Uso de **Regex** para detectar porcentagens, fatoriais e expressões complexas
- **Estilo**: Tailwind CSS via CDN para interface leve e responsiva, sem dependência de build
- **Infraestrutura**: `Docker Compose` com serviço único (`web`) e banco SQLite integrado

---

## 🗂️ Estrutura do Projeto

```
app/
├── calculator/
│   ├── migrations/
│   ├── templates/
│   │   └── calculator/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```

---

## 💡 Observações

- Apenas **operações simples** são salvas no banco SQLite
- Expressões **complexas ou inválidas** são descartadas, mas geram feedback no frontend
- O botão `±` inverte o sinal do último número
- Mensagens de erro/aviso são exibidas de forma clara no topo da página
- Contribuições são bem-vindas via **Issues** ou **Pull Requests**

---

## 📄 Licença

Este projeto está sob a licença MIT.
