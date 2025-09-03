from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, MaintenanceRecord

class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['scheduled_date', 'notes', 'status']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code', 'name', 'category', 'quantity', 'description']

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
