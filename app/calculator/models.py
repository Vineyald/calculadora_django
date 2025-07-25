from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.utils import timezone
from core import settings

# Gerenciador customizado para o modelo de usuário
class UsuarioManager(BaseUserManager):
    # Criação de usuário comum
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("O usuário precisa ter um email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)  # Define a senha de forma segura
        user.save(using=self._db)
        return user

    # Criação de superusuário (admin)
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Modelo customizado de usuário
class Usuario(AbstractBaseUser):
    name = models.CharField(max_length=100)  # Nome do usuário
    email = models.EmailField(unique=True)   # Email único
    dt_inclusao = models.DateTimeField(default=timezone.now)  # Data de inclusão

    is_active = models.BooleanField(default=True)  # Se o usuário está ativo
    is_admin = models.BooleanField(default=False)  # Se é admin

    objects = UsuarioManager()  # Usa o gerenciador customizado

    USERNAME_FIELD = 'email'        # Campo usado para login
    REQUIRED_FIELDS = ['name']      # Campos obrigatórios além do email

    def __str__(self):
        return self.email

    # Permissões (para o Django admin)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

# Modelo para registrar operações da calculadora
class Operacao(models.Model):
    OPERACOES = [
        ('+', 'Soma'),
        ('-', 'Subtração'),
        ('*', 'Multiplicação'),
        ('/', 'Divisão'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usuário dono da operação
    numero1 = models.FloatField()        # Primeiro número
    numero2 = models.FloatField()        # Segundo número
    operacao = models.CharField(max_length=1, choices=OPERACOES)  # Tipo de operação
    resultado = models.FloatField()      # Resultado da operação
    criado_em = models.DateTimeField(auto_now_add=True)  # Data/hora da operação

    def __str__(self):
        return f"{self.numero1} {self.operacao} {self.numero2} = {self.resultado}"
