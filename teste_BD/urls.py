from django.contrib import admin
from django.urls import path, include
from app_teste_BD import views
from django.contrib.auth import views as auth_views
from app_teste_BD.views import chaveamento, registrar_resultado, vencedor_final

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', include('accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inscricao/', views.cadastro, name='inscricao'),
    path('sucesso/', views.sucesso, name='sucessoCadastro'),
    path('chaveamento/', chaveamento, name='chaveamento'),
    path('registrar_resultado/<int:partida_id>/', registrar_resultado, name='registrar_resultado'),
    path('vencedor_final/<str:vencedor_nome>/', vencedor_final, name='vencedor_final'),
    path('', include('app_teste_BD.urls')),
]
