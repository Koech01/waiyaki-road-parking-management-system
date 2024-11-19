from django.contrib import admin
from .models import ParkingColumn, ParkingGrid, Reservation, Notification

admin.site.register(ParkingColumn)
admin.site.register(ParkingGrid)
admin.site.register(Reservation)
admin.site.register(Notification)