from django.contrib import admin
from .models import ParkingLot, Reservation, Notification

admin.site.register(ParkingLot)
admin.site.register(Reservation)
admin.site.register(Notification)