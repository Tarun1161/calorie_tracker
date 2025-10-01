from django import forms
from .models import Consumption

class ConsumptionForm(forms.ModelForm):
    class Meta:
        model = Consumption
        fields = ['food', 'quantity_g']