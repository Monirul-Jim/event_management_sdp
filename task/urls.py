from django.urls import path
from task.views import home
from task.views import category_list, event_list, participant_list, organizer_dashboard, get_event_stats

urlpatterns = [
    path('', home, name='home'),
    path("category/add", category_list, name="create_category"),
    path('events/add', event_list, name='event_list'),
    path('participant/add', participant_list, name='participant_list'),
    path('organizer/', organizer_dashboard, name='dashboard'),
    path('api/event-stats/', get_event_stats, name='get_event_stats'),
]
