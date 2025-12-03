from django.urls import path
from . import views

app_name = 'gym'

urlpatterns = [
    path('', views.gym_list, name='list'),
    path('<int:pk>/', views.gym_detail, name='detail'),
]




