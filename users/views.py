from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from users.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
from task.models import Event, Participant, Category
from task.forms import EventForm, ParticipantForm, CategoryForm
from django.utils import timezone
from django.http import JsonResponse
import users.views
# Create your views here.
# Test for users


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()


def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)


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


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')


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


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def organizer_dashboard(request):
    return render(request, 'organizer/dashboard.html')


@user_passes_test(is_admin_or_organizer, login_url='no-permission')
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


@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def organizer_event(request):
    events = Event.objects.select_related('category').all()
    categories = Category.objects.prefetch_related('events').all()
    event_to_edit = None
    form = EventForm()

    if request.method == "POST":
        if "create" in request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("organizer_event")

        elif "update" in request.POST:
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)

            form = EventForm(request.POST, request.FILES,  instance=event)
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


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(
                request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('change_role')

    return render(request, 'admin/assign_role.html', {"form": form})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(
                request, f"Group {group.name} has been created successfully")
            return redirect('create_group')

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


@user_passes_test(is_admin, login_url='no-permission')
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


@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == "POST":
        group.delete()
        messages.success(
            request, f"Group '{group.name}' has been deleted successfully.")
        return redirect('group_list')  # Redirect to the groups list page

    return render(request, 'admin/delete_group.html', {"group": group})


@user_passes_test(is_admin, login_url='no-permission')
def delete_participant(request):
    events = Event.objects.prefetch_related("participants__user").all()
    return render(request, 'admin/delete_participants.html', {"events": events})


@user_passes_test(is_admin, login_url='no-permission')
def remove_participant(request, event_id, participant_id):
    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(Participant, id=participant_id)

    participant.events.remove(event)

    if participant.events.count() == 0:
        participant.delete()

    messages.success(
        request, f"{participant.user.username} has been removed from {event.name}.")
    return redirect('delete_participant')


@user_passes_test(is_admin, login_url='no-permission')
def remove_all_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    event.participants.clear()

    messages.success(
        request, f"All participants have been removed from {event.name}.")
    return redirect('delete_participant')


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


@login_required
def participant_joined_event(request):
    # Get the participant instance for the logged-in user
    try:
        # Using 'participant_profile' as related_name
        participant = request.user.participant_profile
        # Get all events the participant is in
        participant_events = participant.events.all()
    except Participant.DoesNotExist:
        participant_events = []  # If the user doesn't have a participant profile yet

    return render(request, 'participant/participant_joined_event.html', {'events': participant_events})
