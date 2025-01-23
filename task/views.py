from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView

from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.shortcuts import redirect


def category_list(request):
    categories = Category.objects.all()
    form = CategoryForm()
    category_to_edit = None  # To determine if we are editing

    if request.method == "POST":
        if "create" in request.POST:  # Handle new category creation
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("create_category")

        elif "update" in request.POST:  # Handle category update
            category_id = request.POST.get("category_id")
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect("create_category")

        elif "delete" in request.POST:  # Handle category deletion
            category_id = request.POST.get("category_id")
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect("create_category")

        elif "update_form" in request.POST:  # Pre-fill the form for editing
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
    categories = Category.objects.all()  # Fetch all categories
    event_to_edit = None  # To determine if we are editing
    form = EventForm()  # Initialize the form

    if request.method == "POST":
        if "create" in request.POST:  # Handle new event creation
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("event_list")  # Redirect to the event list

        elif "update" in request.POST:  # Handle event update
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)
            # Populate form with existing event data
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect("event_list")  # Redirect to the event list

        elif "delete" in request.POST:  # Handle event deletion
            event_id = request.POST.get("event_id")
            event = get_object_or_404(Event, id=event_id)
            event.delete()
            return redirect("event_list")  # Redirect to the event list

        elif "update_form" in request.POST:  # Pre-fill the form for editing
            event_id = request.POST.get("event_id")
            event_to_edit = get_object_or_404(Event, id=event_id)
            # Populate form with existing event data
            form = EventForm(instance=event_to_edit)

    # Render the template with the context
    return render(request, "task/create_event.html", {
        "events": events,
        "form": form,
        "event_to_edit": event_to_edit,
        "categories": categories  # Pass categories to the template
    })


def participant_list(request):
    participants = Participant.objects.all()
    form = ParticipantForm()
    participant_to_edit = None  # To determine if we are editing

    if request.method == "POST":
        if "create" in request.POST:  # Handle new participant creation
            form = ParticipantForm(request.POST)
            if form.is_valid():
                form.save()
                # Redirect to the participant list
                return redirect("participant_list")

        elif "update" in request.POST:  # Handle participant update
            participant_id = request.POST.get("participant_id")
            participant = get_object_or_404(Participant, id=participant_id)
            # Populate form with existing participant data
            form = ParticipantForm(request.POST, instance=participant)
            if form.is_valid():
                form.save()
                # Redirect to the participant list
                return redirect("participant_list")

        elif "delete" in request.POST:  # Handle participant deletion
            participant_id = request.POST.get("participant_id")
            participant = get_object_or_404(Participant, id=participant_id)
            participant.delete()
            # Redirect to the participant list
            return redirect("participant_list")

        elif "update_form" in request.POST:  # Pre-fill the form for editing
            participant_id = request.POST.get("participant_id")
            participant_to_edit = get_object_or_404(
                Participant, id=participant_id)
            # Populate form with existing participant data
            form = ParticipantForm(instance=participant_to_edit)

    return render(request, "task/create_participant.html", {
        "participants": participants,
        "form": form,
        "participant_to_edit": participant_to_edit,
        "events": Event.objects.all()  # Pass all events to the template for selection
    })


def home(request):
    return render(request, 'home.html')
