from django.contrib import admin
from django.urls import path
from calculator import views
from calculator.views import calculadora_view, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', calculadora_view, name='calculadora'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('limpar_historico/', views.limpar_historico, name='limpar_historico'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
]
