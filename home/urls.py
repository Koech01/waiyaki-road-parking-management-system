from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('createParkingGrid/', views.createParkingGrid, name='createParkingGrid'),
    path('reserveParkingGrid/<int:slotId>/', views.reserveParkingGrid, name='reserveParkingGrid')
]