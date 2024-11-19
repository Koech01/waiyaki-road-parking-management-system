from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('createParkingGrid/', views.createParkingGrid, name='createParkingGrid'),
    path('increaseParkingColumns/', views.increaseParkingColumns, name='increaseParkingColumns'),
    path('decreaseParkingColumns/', views.decreaseParkingColumns, name='decreaseParkingColumns'),
    path('reserveParkingGrid/<int:slotId>/', views.reserveParkingGrid, name='reserveParkingGrid')
]