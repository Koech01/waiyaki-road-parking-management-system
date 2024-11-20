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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    row = models.IntegerField()
    column = models.IntegerField()
    slotNo = models.CharField(max_length=10, unique=True)
    isAvailable = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Check for the last parking grid to determine the next row/column
        lastParkingGrid = ParkingGrid.objects.last()

        if lastParkingGrid:
            # Use the last row and column to determine the next slot
            lastRow = lastParkingGrid.row
            lastColumn = lastParkingGrid.column
            totalColumns = ParkingColumn.objects.first().totalColumn

            # Move to the next row if the last column has been reached
            if lastColumn >= totalColumns:
                self.row = lastRow + 1
                self.column = 1
            else:
                self.row = lastRow
                self.column = lastColumn + 1
        else:
            # For the first parking grid, initialize row and column
            self.row = 1
            self.column = 1

        # Generate the unique slot number based on row and column
        self.slotNo = f"R{self.row}C{self.column}"

        # Ensure row and column are not null before saving
        if self.row is None or self.column is None:
            raise ValueError("Row and Column must be set before saving.")

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Id {self.id} - Row {self.row}, Column {self.column} - {'Available' if self.isAvailable else 'Reserved'}"


    class Meta:
        unique_together = ('row', 'column')


class Reservation(models.Model):
    user      = models.ForeignKey(Profile, on_delete=models.CASCADE)
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

    def cancel(self):
        self.isActive = False
        self.parkingSlot.isAvailable = True
        self.parkingSlot.save()
        self.save()

    def __str__(self):
        return f"User: {self.user.user} CarPlate {self.carPlate}, isActive {self.isActive}"


class Notification(models.Model):
    carPlate  = models.CharField(max_length=15)
    user      = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message   = models.TextField()
    startTime = models.DateTimeField()
    endTime   = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.user.username} : {self.message}"