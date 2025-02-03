
from django.urls import path
from users.views import user_login, user_register, user_logout, admin_dashboard
urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('user-logout/', user_logout, name='logout'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]
