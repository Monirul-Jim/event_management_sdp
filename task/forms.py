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
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'placeholder': 'Enter category name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Enter category description',
            }),
        }
