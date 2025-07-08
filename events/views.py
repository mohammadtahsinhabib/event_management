from django.shortcuts import render, redirect
from events.models import Event, Category, Participant
from events.forms import EventForm, CategoryForm, ParticipantForm
from django.db.models import Q , Count
from django.contrib import messages
from datetime import date


def organizer_dashboard(request):
    base_query = Event.objects.all()

    total_participants = Participant.objects.count()
    total_events = base_query.count()
    upcoming_events = base_query.filter(date__gt =date.today()).count()
    past_events = base_query.filter(date__lt=date.today()).count()
    
    filter = request.GET.get("filter")
    
    if filter == "upcoming":
        events = base_query.filter(date__gte=date.today())
        title = "Upcoming Events"
    elif filter == "past":
        events = base_query.filter(date__lt=date.today())
        title = "Past Events"
    elif filter == "total":
        events = base_query
        title = "All Events"
    else:
        events = base_query.filter(date=date.today())
        title = "Today's Events"

    context = {
        "total_participants": total_participants,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "events": events,
        "title": title,
    }
    return render(request, "dashboard.html", context)



def category_list(request):
    category = Category.objects.all()
    return render(request, "category/list.html", {"categories": category})

def category_create(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category Added Successfully")
            return redirect("category-list")
        
        else: messages.error(request, "Something Went Wrong")

    return render(request, "category/form.html", {"form": form})

def category_update(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)

    if request.method == "POST":
        form = CategoryForm(request.POST , instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,"Category Updated Successfully")
            return redirect("category-list")
        
    return render(request, "category/form.html", {"form": form})

def category_delete(request, id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request,"Category Deleted Successfully")
    
    return redirect("category-list")


def event_detail(request, id):
    event = Event.objects.select_related("category").get(id=id)
    return render(request, "events/detail.html", {"event": event})

def event_list(request):
    query = request.GET.get("q", "")
    base_query = Event.objects.select_related("category")

    if query:
        events = base_query.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events =base_query.all()
    
    events = base_query.annotate(participant_count = Count("participant"))

    return render(request, "events/list.html", { "events" : events})

def event_create(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Added Successfully")
            return redirect("event-list")
        
        else: messages.error(request, "Something Went Wrong")

    return render(request, "events/form.html", {"form": form})


def event_update(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(instance=event)

    if request.method == "POST":
        form = EventForm(request.POST , instance=event)
        if form.is_valid():
            form.save()
            messages.success(request,"Event Updated Successfully")
            return redirect("event-list")
        
    return render(request, "events/form.html", {"form": form})

def event_delete(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
    
    return redirect("event-list")


def participant_list(request):
    participants = Participant.objects.prefetch_related("events").all()
    
    return render(request, "participant/list.html", {"participants": participants})

def participant_create(request):
    form = ParticipantForm()
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Participant Added Successfully")
            return redirect("participant-list")
        
        else: messages.error(request, "Something Went Wrong")

    return render(request, "participant/form.html", {"form": form})

def participant_update(request, id):
    participant = Participant.objects.prefetch_related("events").get(id=id)
    form = ParticipantForm(instance=participant)

    if request.method == "POST":
        form = ParticipantForm(request.POST , instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request,"Participant Updated Successfully")
            return redirect("participant-list")
        
    return render(request, "participant/form.html", {"form": form})

def participant_delete(request, id):
    if request.method == "POST":
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.success(request,"Participant Deleted Successfully")
    
    return redirect("participant-list")
