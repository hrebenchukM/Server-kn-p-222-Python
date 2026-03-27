from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('transfer/', views.transfer, name='transfer'),
    path('static-page/', views.static_page, name='static'),
    path('forms/', views.forms, name='forms'),
    path('models/', views.models, name='models'),
]