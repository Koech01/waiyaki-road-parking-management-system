from django.contrib import admin
from .models import ParkingGrid, Reservation, Notification

admin.site.register(ParkingGrid)
admin.site.register(Reservation)
admin.site.register(Notification)