from django import forms
from datetime import timedelta
from .models import Reservation
from django.core.exceptions import ValidationError

class ReservationForm(forms.ModelForm):
    carPlate = forms.CharField(label="Car Plate", required=False, max_length=15)

    startTime = forms.DateTimeField(
        widget   = forms.DateTimeInput(attrs={'placeholder': 'Start Date and Time', 'type': 'datetime-local'}),
        required = True
    )
    endTime = forms.DateTimeField(
        widget   = forms.DateTimeInput(attrs={'placeholder': 'End Date and Time', 'type': 'datetime-local'}),
        required = True
    )

    class Meta:
        model  = Reservation
        fields = ['carPlate', 'startTime', 'endTime']

    def clean(self):
        cleaned_data = super().clean()
        startTime    = cleaned_data.get('startTime')
        endTime      = cleaned_data.get('endTime')

        # Ensure start time is before end time
        if startTime and endTime:
            if startTime >= endTime:
                raise ValidationError("Start time must be before the end time.")

            # Ensure the reservation duration is within 18 hours
            if (endTime - startTime) > timedelta(hours=18):
                raise ValidationError("Reservation duration cannot exceed 18 hours.")
        
        return cleaned_data
