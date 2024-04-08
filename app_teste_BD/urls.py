from app_teste_BD import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'), 

]