from django.db import models
from datetime import timedelta
from django.utils import timezone
from profiles.models import Profile

# Create your models here.
class ParkingColumn(models.Model):
    totalColumn = models.IntegerField(default=0)

    def __str__(self):
        return f"ParkingGrid - Columns: {self.totalColumn}"


class ParkingGrid(models.Model):
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    row         = models.IntegerField()
    column      = models.IntegerField()
    startTime   = models.DateTimeField(blank=True, null=True)  # Allow blank/empty
    endTime     = models.DateTimeField(blank=True, null=True)   
    slotNo      = models.CharField(max_length=10, unique=True)
    isAvailable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.startTime is None:
            self.startTime = timezone.now()
        if self.endTime is None:
            self.endTime = timezone.now() + timedelta(hours=1)  # Example: 1 hour later

        lastParkingGrid = ParkingGrid.objects.last()
        if lastParkingGrid:
            lastRow      = lastParkingGrid.row
            lastColumn   = lastParkingGrid.column
            totalColumns = ParkingColumn.objects.first().totalColumn

            if lastColumn >= totalColumns:
                self.row    = lastRow + 1
                self.column = 1
            else:
                self.row    = lastRow
                self.column = lastColumn + 1
        else:
            self.row    = 1
            self.column = 1

        self.slotNo = f"R{self.row}C{self.column}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Id {self.id} - Row {self.row}, Column {self.column} - {'Available' if self.isAvailable else 'Reserved'}"


    class Meta:
        unique_together = ('row', 'column')


class Reservation(models.Model):
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parkingSlot = models.ForeignKey(ParkingGrid, on_delete=models.CASCADE)
    isActive    = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.user} Slot: Row {self.parkingSlot.row}, Column {self.parkingSlot.column}"

    def cancel(self):
        self.isActive = False
        self.parkingSlot.isAvailable = True
        self.parkingSlot.save()
        self.save()


class Notification(models.Model):
    user      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.user.username} : {self.message}"