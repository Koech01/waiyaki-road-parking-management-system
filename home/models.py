from django.db import models
from profiles.models import Profile

# Create your models here.
class ParkingLot(models.Model):
    slotNo      = models.CharField(max_length=10, unique=True) 
    isAvailable = models.BooleanField(default=True)         

    def __str__(self):
        return f"Slot: {self.slotNo} - {'Available' if self.isAvailable else 'Reserved'}"


class Reservation(models.Model):
    user       = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parkingLot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    startTime  = models.DateTimeField()
    endTime    = models.DateTimeField()
    isActive   = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.user} Slot:  {self.parkingLot.slotNo}"

    def cancel(self):
        self.is_active = False
        self.parking_lot.is_available = True
        self.parking_lot.save()
        self.save()


class Notification(models.Model):
    user      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.user.username} : {self.message}"