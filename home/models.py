from django.db import models
from datetime import timedelta
from profiles.models import Profile
from django.core.exceptions import ValidationError


# Create your models here.
class ParkingColumn(models.Model):
    totalColumn = models.IntegerField(default=0)

    def __str__(self):
        return f"ParkingGrid - Columns: {self.totalColumn}"


class ParkingGrid(models.Model):
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    row         = models.IntegerField()
    column      = models.IntegerField()
    slotNo      = models.CharField(max_length=10, unique=True)
    isAvailable = models.BooleanField(default=True)


    def __str__(self):
        return f"Id {self.id} - Row {self.row}, Column {self.column} - {'Available' if self.isAvailable else 'Reserved'}"


    class Meta:
        unique_together = ('row', 'column')


class Reservation(models.Model):
    user      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slot      = models.ForeignKey(ParkingGrid, on_delete=models.CASCADE, blank=True, null=True)
    carPlate  = models.CharField(max_length=15)
    startTime = models.DateTimeField()
    endTime   = models.DateTimeField()
    isActive  = models.BooleanField(default=True)

    def clean(self):
        if self.startTime and self.endTime:
            if self.startTime >= self.endTime:
                raise ValidationError("Start time must be before the end time.")

            # Ensure reservation duration is within 18 hours
            if (self.endTime - self.startTime) > timedelta(hours=18):
                raise ValidationError("Reservation duration cannot exceed 18 hours.")
        else:
            raise ValidationError("Start time and end time are required.")

    def __str__(self):
        return f"User: {self.user.user} CarPlate {self.carPlate}, isActive {self.isActive}"


class Notification(models.Model):
    carPlate    = models.CharField(max_length=15)
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message     = models.TextField()
    startTime   = models.DateTimeField()
    endTime     = models.DateTimeField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    isCancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user.user.username} : {self.message}"