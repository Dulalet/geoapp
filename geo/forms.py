from django import forms
from .models import Building, BusStop, Street, RedLine

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'


class BusStopForm(forms.ModelForm):
    class Meta:
        model = BusStop
        fields = '__all__'

class StreetForm(forms.ModelForm):
    class Meta:
        model = Street
        fields = '__all__'


class RedLineForm(forms.ModelForm):
    class Meta:
        model = RedLine
        fields = '__all__'

