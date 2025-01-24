from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView

from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from datetime import date


def category_list(request):
    categories = Category.objects.all()
    form = CategoryForm()
    category_to_edit = None

    if request.method == "POST":
        if "create" in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("create_category")

        elif "update" in request.POST:
            category_id = request.POST.get("category_id")
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect("create_category")

        elif "delete" in request.POST:
            category_id = request.POST.get("category_id")
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect("create_category")

        elif "update_form" in request.POST:
            category_id = request.POST.get("category_id")
            category_to_edit = get_object_or_404(Category, id=category_id)
            form = CategoryForm(instance=category_to_edit)

    return render(request, "task/create_category.html", {
        "categories": categories,
        "form": form,
        "category_to_edit": category_to_edit
    })


def event_list(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    event_to_edit = None
    form = EventForm()

    if request.method == "POST":
        if "create" in request.POST:
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("event_list")

        elif "update" in request.POST:
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)

            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect("event_list")

        elif "delete" in request.POST:
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            return redirect("event_list")

        elif "update_form" in request.POST:
            event_id = request.POST.get("event_id")
            event_to_edit = get_object_or_404(Event, id=event_id)

            form = EventForm(instance=event_to_edit)

    return render(request, "task/create_event.html", {
        "events": events,
        "form": form,
        "event_to_edit": event_to_edit,
        "categories": categories
    })


def participant_list(request):
    participants = Participant.objects.all()
    form = ParticipantForm()
    participant_to_edit = None

    if request.method == "POST":
        if "create" in request.POST:
            form = ParticipantForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("participant_list")

        elif "update" in request.POST:
            participant_id = request.POST.get("participant_id")
            participant = get_object_or_404(Participant, id=participant_id)
            form = ParticipantForm(request.POST, instance=participant)
            if form.is_valid():
                form.save()
                return redirect("participant_list")

        elif "delete" in request.POST:
            participant_id = request.POST.get("participant_id")
            participant = get_object_or_404(Participant, id=participant_id)
            participant.delete()
            return redirect("participant_list")

        elif "update_form" in request.POST:
            participant_id = request.POST.get("participant_id")
            participant_to_edit = get_object_or_404(
                Participant, id=participant_id)
            form = ParticipantForm(instance=participant_to_edit)

    return render(request, "task/create_participant.html", {
        "participants": participants,
        "form": form,
        "participant_to_edit": participant_to_edit,
        "events": Event.objects.all()
    })


def organizer_dashboard(request):
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

    return render(request, 'task/dashboard.html', context)


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


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.all()
    return render(request, 'event_detail.html', {'event': event, 'participants': participants})


# def home(request):

#     events = Event.objects.annotate(
#         participant_count=Count('participants')).all()
#     for i in events:
#         print(i)
#     return render(request, 'home.html', {'events': events})
def home(request):
    # Get today's date
    today = date.today()

    # Get all events and annotate with participant count
    events = Event.objects.annotate(
        participant_count=Count('participants')).all()

    # Filter upcoming events (events that are on or after today's date)
    upcoming_events = Event.objects.filter(date__gte=today).annotate(
        participant_count=Count('participants')).order_by('date')

    return render(request, 'home.html', {'events': events, 'upcoming_events': upcoming_events})


def search_events(request):
    query = request.GET.get('search', '')
    events = Event.objects.filter(
        Q(name__icontains=query) | Q(location__icontains=query)
    ) if query else Event.objects.none()
    return render(request, 'task/search_results.html', {'events': events, 'query': query})
