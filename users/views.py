from django.shortcuts import render, get_object_or_404
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
from task.models import Event, Participant, Category
from task.forms import EventForm, ParticipantForm, CategoryForm
from django.utils import timezone
from django.http import JsonResponse
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


# def admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')

@login_required
def dashboard_redirect(request):
    user = request.user

    if user.groups.filter(name="Admin").exists():
        return redirect('admin_dashboard')
    elif user.groups.filter(name="Organizer").exists():
        return redirect('organizer_dashboard')
    elif user.groups.filter(name="Participant").exists():
        return redirect('participant_dashboard')
    else:
        return redirect('home')


@login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


@login_required
def organizer_dashboard(request):
    return render(request, 'organizer/dashboard.html')


def organizer_category(request):
    categories = Category.objects.all()
    form = CategoryForm()
    category_to_edit = None

    if request.method == "POST":
        if "create" in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("organizer_category")

        elif "update" in request.POST:
            category_id = request.POST.get("category_id")
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect("organizer_category")

        elif "delete" in request.POST:
            category_id = request.POST.get("category_id")
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect("organizer_category")

        elif "update_form" in request.POST:
            category_id = request.POST.get("category_id")
            category_to_edit = get_object_or_404(Category, id=category_id)
            form = CategoryForm(instance=category_to_edit)

    return render(request, "organizer/organizer_category.html", {
        "categories": categories,
        "form": form,
        "category_to_edit": category_to_edit
    })


def organizer_event(request):
    events = Event.objects.select_related('category').all()
    categories = Category.objects.prefetch_related('events').all()
    event_to_edit = None
    form = EventForm()

    if request.method == "POST":
        if "create" in request.POST:
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("organizer_event")

        elif "update" in request.POST:
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)

            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect("organizer_event")

        elif "delete" in request.POST:
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            return redirect("organizer_event")

        elif "update_form" in request.POST:
            event_id = request.POST.get("event_id")
            event_to_edit = get_object_or_404(Event, id=event_id)

            form = EventForm(instance=event_to_edit)

    return render(request, "organizer/organizer_event.html", {
        "events": events,
        "form": form,
        "event_to_edit": event_to_edit,
        "categories": categories
    })


@login_required
def participant_dashboard(request):
    return render(request, 'participant/dashboard.html')


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
            return redirect('change_role')

    return render(request, 'admin/assign_role.html', {"form": form})


def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('create_group')

    return render(request, 'admin/create_group.html', {'form': form})


def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


def change_role(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/change_role.html', {"users": users})


def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == "POST":
        group.delete()
        messages.success(request, f"Group '{
                         group.name}' has been deleted successfully.")
        return redirect('group_list')  # Redirect to the groups list page

    return render(request, 'admin/delete_group.html', {"group": group})


def delete_participant(request):
    return render(request, 'admin/delete_participants.html')


def organizer_dashboard_stats(request):
    today = timezone.now().date()

    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()

    todays_events = Event.objects.filter(date=today)

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    }

    return render(request, 'organizer/stats.html', context)


def get_event_stats(request):
    today = timezone.now().date()

    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()

    data = {
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return JsonResponse(data)


def get_events(request):
    event_type = request.GET.get('type', 'all')
    today = timezone.now().date()

    if event_type == 'upcoming':
        events = Event.objects.filter(date__gt=today)
    elif event_type == 'past':
        events = Event.objects.filter(date__lt=today)
    else:
        events = Event.objects.all()

    event_list = [{
        'name': event.name,
        'date': event.date,
        'time': event.time,
        'location': event.location,
    } for event in events]

    return JsonResponse({'events': event_list})

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
