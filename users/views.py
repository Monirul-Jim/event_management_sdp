from django.shortcuts import render
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
# Create your views here.


def user_register(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('register')

        else:
            print("Form is not valid")
    return render(request, 'users/register.html', {"form": form})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    print(users)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {"users": users})


def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})


def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


# from django.shortcuts import render, redirect
# from users.forms import CustomRegistrationForm
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.urls import reverse
# from django.core.mail import send_mail
# from django.conf import settings
# User = get_user_model()


# def user_login(request):
#     return render(request, 'users/login.html')


# def user_register(request):
#     form = CustomRegistrationForm()
#     if request.method == 'POST':
#         form = CustomRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data.get('password1'))
#             user.is_active = False  # Initially inactive
#             user.save()

#             # Generate token and uid
#             uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)

#             # Build activation link
#             activation_link = request.build_absolute_uri(
#                 reverse('activate', kwargs={'uidb64': uidb64, 'token': token}))

#             # Send email
#             subject = 'Activate Your Account'
#             message = f'Dear {user.username},\n\nPlease click on the link below to activate your account:\n\n{
#                 activation_link}\n\nIf you did not register, you can safely ignore this email.'
#             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
#                       [user.email])  # Use your email settings

#             messages.success(
#                 request, 'A confirmation email has been sent. Please check your inbox to activate your account.')
#             return redirect('register')

#         else:
#             # Keep this for debugging, but consider a better logging method in production
#             print("Form is not valid")
#             # Add form errors to the template context so the user sees them
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field.capitalize()}: {
#                                    error}")  # Display errors to the user

#     return render(request, 'users/register.html', {"form": form})


# def activate(request, uidb64, token):
#     try:
#         uid = force_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(
#             request, 'Your account has been activated. You can now log in.')
#         return redirect('login')  # Redirect to login page
#     else:
#         messages.error(request, 'Invalid activation link.')
#         return redirect('register')  # Or another appropriate page
