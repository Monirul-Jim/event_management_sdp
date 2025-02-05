from django.urls import path
from task.views import home
from task.views import (category_list, event_list,
                        participant_list, organizer_dashboard,
                        get_event_stats, get_events, event_detail,
                        search_events,
                        join_event

                        )

urlpatterns = [
    path('', home, name='home'),
    path("category/add", category_list, name="create_category"),
    path('event/<int:event_id>/join/', join_event, name='join_event'),
    path('events/add', event_list, name='event_list'),
    path('participant/add', participant_list, name='participant_list'),
    path('organizer/', organizer_dashboard, name='dashboard'),
    path('api/event-stats/', get_event_stats, name='get_event_stats'),
    path('api/events/', get_events, name='get_events'),
    path('event-details/<int:event_id>/', event_detail, name='event_detail'),
    path('search/', search_events, name='search_events'),
]
