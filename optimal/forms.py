from django import forms
from .models import WellnessPackage, Category

class WellnessPackageForm(forms.ModelForm):
    class Meta:
        model = WellnessPackage
        fields = ['title', 'description', 'image', 'price', 'category']
