from django import forms
from .models import Location, Farm, Farmer, Resource, AnimalType, Animal

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'size', 'location']

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'quantity', 'expiration_date', 'farm_resource']

class AnimalTypeForm(forms.ModelForm):
    class Meta:
        model = AnimalType
        fields = ['name']

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['gender', 'health_status', 'resources', 'animal_type']
