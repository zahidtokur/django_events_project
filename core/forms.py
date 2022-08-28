from django.utils import timezone
from django.forms import ModelForm, DateInput, ValidationError

from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date"]
        widgets = {
            'date': DateInput(
                attrs={'type': 'date'}),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past!")
        return date
