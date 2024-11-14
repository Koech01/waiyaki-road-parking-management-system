from django import forms
from .models import Profile, CarPlate


class EditForm(forms.ModelForm):
    firstName = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    lastName  = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email     = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    carPlates = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter car plates separated by commas', 'size': '40'}),
        help_text="Enter car plates separated by commas, e.g. ABC123, XYZ789"
    )

    class Meta:
        model   = Profile
        fields  = ('profilePicture', 'firstName', 'lastName', 'email')

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.cleaned_data['carPlates']:
            plates = self.cleaned_data['carPlates'].split(',')
            for plate in plates:
                CarPlate.objects.create(profile=instance, plateNumber=plate.strip())
        
        if commit:
            instance.save()
        return instance
