from django.forms import ModelForm, DateInput
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date"]
        widgets = {
            'date': DateInput(
                attrs={'type': 'date'}),
        }
