

from django.urls import path
from users.views import (UserLoginView, UserRegisterView, ActivateUserView,
                         user_logout, create_group,
                         change_role, group_list,
                         delete_group, delete_participant,
                         AssignRoleView, DashboardRedirectView,
                         admin_dashboard,
                         organizer_dashboard,
                         participant_dashboard,
                         organizer_category,
                         organizer_event,
                         get_event_stats,
                         organizer_dashboard_stats,
                         participant_joined_event,
                         remove_participant,
                         remove_all_participants,
                         ProfileViews,
                         ChangePassword,
                         CustomPasswordResetView,
                         CustomPasswordResetConfirmView,
                         EditProfileView
                         )
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('user-logout/', user_logout, name='logout'),
    path('activate/<int:user_id>/<str:token>/', ActivateUserView.as_view()),
    path('dashboard/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('organizer/dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('organizer/organizer-category/',
         organizer_category, name='organizer_category'),
    path('organizer/organizer-event/',
         organizer_event, name='organizer_event'),
    path('organizer/stats', organizer_dashboard_stats,
         name='organizer_dashboard_stats'),
    path('organizer/organizer-event-stats/',
         get_event_stats, name='get_event_stats'),
    path('participant/dashboard/', participant_dashboard,
         name='participant_dashboard'),
    path('participant/dashboard/joined-event', participant_joined_event,
         name='participant_joined'),
    path('admin/create-group/', create_group, name='create_group'),
    path('admin/change-role/', change_role, name='change_role'),
    path('admin/group-list/', group_list, name='group_list'),
    path('admin/delete-group/<int:group_id>/',
         delete_group, name='delete_group'),
    path('admin/delete-participants/',
         delete_participant, name='delete_participant'),
    path('event/<int:event_id>/remove-participant/<int:participant_id>/',
         remove_participant, name='remove_participant'),
    path('event/<int:event_id>/remove-all-participants/',
         remove_all_participants, name='remove_all_participants'),
    path('admin/<int:user_id>/assign-role/',
         AssignRoleView.as_view(), name='assign_role'),
    path('user/profile', ProfileViews.as_view(), name='profile'),
    path('password-change/',
         ChangePassword.as_view(), name='password_change'),
    #     path('password-change/',
    #          PasswordChangeView.as_view(template_name='account/password_change.html'), name='password_change'),
    path('password-change-done/',
         PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('password-reset/',
         CustomPasswordResetView.as_view(), name='reset_password'),
    path('password-reset/confirm/<uidb64>/<token>',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')
]
