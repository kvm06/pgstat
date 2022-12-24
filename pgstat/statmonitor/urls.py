from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query/<int:stat_id>/', views.query, name='query'),
]