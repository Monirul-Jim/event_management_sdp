from django.contrib import admin
from task.models import Category, Event, Participant
# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Participant)
