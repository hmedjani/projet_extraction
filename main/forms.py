from django import forms
from .models import ImageModel

class PhotoForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']
