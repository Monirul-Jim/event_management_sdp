from django import forms
from .models import Event, Participant, Category


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
