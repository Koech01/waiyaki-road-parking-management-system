from django import forms
from .models import Profile, CarPlate


class EditForm(forms.ModelForm):
    firstName = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lastName  = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email     = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    carPlates = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter car plates separated by commas', 'size': '40'}),
        help_text="Enter car plates separated by commas, e.g. KBB 123A, KBC 345B"
    )

    class Meta:
        model   = Profile
        fields  = ('profilePicture', 'firstName', 'lastName', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.carPlates:
            # Join the car plates into a comma-separated string for display
            self.fields['carPlates'].initial = ', '.join([plate.plateNumber for plate in self.instance.car_plates.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data['carPlates']:
            plates = self.cleaned_data['carPlates'].split(',')
            # Remove existing car plates before saving new ones
            instance.car_plates.all().delete()  # Optional: remove old car plates before adding new ones
            for plate in plates:
                CarPlate.objects.create(profile=instance, plateNumber=plate.strip())
        
        if commit:
            instance.save()
        return instance