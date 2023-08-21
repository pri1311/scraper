from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAbout),
    path('extract/', views.extract, name='extract')
]