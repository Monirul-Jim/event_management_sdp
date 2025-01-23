from django.urls import path
from task.views import home
urlpatterns = [
    path('', home, name='home'),
]
