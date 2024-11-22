from . import views
from django.urls import path

app_name = 'home'

urlpatterns = [
    path('', views.homeView, name='home'),
    path('createParkingGrid/', views.createParkingGrid, name='createParkingGrid'),
    path('removeParkingGrid/', views.removeParkingGrid, name='removeParkingGrid'),
    path('increaseParkingColumns/', views.increaseParkingColumns, name='increaseParkingColumns'),
    path('decreaseParkingColumns/', views.decreaseParkingColumns, name='decreaseParkingColumns'),
    path('reserveParkingGrid/<int:slotId>/', views.reserveParkingGrid, name='reserveParkingGrid'),
    path('reservationDetail/<int:slotId>/', views.reservationDetail, name='reservationDetail'),
    path('reservationCancel/<int:slotId>/', views.cancelReservation, name='reservationCancel')
]