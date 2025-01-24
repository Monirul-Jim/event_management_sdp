from django import forms
from .models import Event, Participant, Category
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = '__all__'

from django.core.exceptions import ValidationError
from django.utils.timezone import now


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.startswith(('http://', 'https://')):
            raise ValidationError("Please provide a valid URL for the image.")
        return image

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError(
                "Event name must be at least 3 characters long.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError(
                "Event description must be at least 10 characters long.")
        return description

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < now().date():
            raise ValidationError("The event date cannot be in the past.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if not time:
            raise ValidationError("Event time is required.")
        return time

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if len(location) < 3:
            raise ValidationError(
                "Location must be at least 3 characters long.")
        return location

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError("Please select a valid category.")
        return category


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError(
                "Participant name must be at least 3 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email is required.")
        if Participant.objects.filter(email=email).exists():
            raise ValidationError(
                "A participant with this email already exists.")
        return email

    def clean_events(self):
        events = self.cleaned_data.get('events')
        if not events:
            raise ValidationError("At least one event must be selected.")
        return events


# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'description']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
#                 'placeholder': 'Enter category name',
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'mt-1 p-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
#                 'rows': 4,
#                 'placeholder': 'Enter category description',
#             }),
#         }
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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError(
                "Category name must be at least 3 characters long.")
        if Category.objects.filter(name__iexact=name).exists():
            raise ValidationError("A category with this name already exists.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError(
                "Category description must be at least 10 characters long.")
        return description
