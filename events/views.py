from django.shortcuts import (
    render,
    redirect,
    HttpResponse,
    HttpResponseRedirect,
    get_object_or_404,
)
from django.urls import reverse
from django.contrib import messages
from events.models import Event, Category
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.tokens import default_token_generator
from events.forms import EventForm, CategoryForm, SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()


@user_passes_test(is_admin, login_url="/no-permission/")
def admin_dashboard(request):
    context = {
        "users": User.objects.all(),
        "groups": Group.objects.all(),
        "events": Event.objects.all(),
        "is_admin": True,
        "is_organizer": False,
        "is_participant": False,
    }
    return render(request, "dashboard/admin.html", context)


@login_required
@user_passes_test(is_admin, login_url="/no-permission/")
def change_user_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    groups = Group.objects.exclude(name="Admin")

    if request.method == "POST":
        selected_group_name = request.POST.get("group")
        if selected_group_name:
            selected_group = Group.objects.get(name=selected_group_name)
            user.groups.clear()
            user.groups.add(selected_group)
            messages.success(
                request, f"Role for {user.username} changed to {selected_group.name}"
            )
            return redirect("admin-dashboard")

    return render(
        request, "dashboard/change_role.html", {"user_obj": user, "groups": groups}
    )


@login_required
@user_passes_test(is_admin, login_url="/no-permission/")
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Group.objects.get_or_create(name=name)
            messages.success(request, f"Group '{name}' created successfully")
    return redirect("admin-dashboard")


@login_required
@user_passes_test(is_admin, login_url="/no-permission/")
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect("admin-dashboard")


@login_required
@user_passes_test(is_admin, login_url="/no-permission/")
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if group.name != "Admin":
        group.delete()
        messages.success(request, f"Group '{group.name}' deleted.")
    return redirect("admin-dashboard")


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def organizer_dashboard(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        "dashboard/organizer.html",
        {
            "events": events,
            "categories": categories,
            "is_admin": False,
            "is_organizer": True,
            "is_participant": False,
        },
    )


@user_passes_test(
    lambda user: is_admin(user) or is_participant(user), login_url="/no-permission/"
)
def participants_dashboard(request):
    events = request.user.rsvped_events.all()
    return render(
        request,
        "dashboard/participant.html",
        {
            "events": events,
            "is_admin": False,
            "is_organizer": False,
            "is_participant": True,
        },
    )


@user_passes_test(is_participant, login_url="/no-permission/")
def view_events(request):

    events = Event.objects.all()
    return render(request, "participant/view_events.html", {"events": events})


@login_required
def dashboard_redirect(request):
    if is_admin(request.user):
        return redirect("admin-dashboard")
    elif is_organizer(request.user):
        return redirect("organizer-dashboard")
    elif is_participant(request.user):
        return redirect("participants-dashboard")

    return redirect("no-permission")


def sign_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.is_active = False
            user.save()
            group = Group.objects.get(name="Participant")
            user.groups.add(group)

            messages.success(request, "A congirmation email sent to your email")
            return redirect("sign-in")

    return render(request, "registration/sign_up.html", {"form": form})


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid Id or token")

    except User.DoesNotExist:
        return HttpResponse("User not found")


def sign_in(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")

    return render(request, "registration/sign_in.html", {"form": form})


@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)

    return redirect("sign-in")


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def category_create(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Added Successfully")
            return HttpResponseRedirect(reverse("organizer-dashboard") + "#categories")

        else:
            messages.error(request, "Something Went Wrong")

    return render(request, "category/form.html", {"form": form})


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def category_update(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return HttpResponseRedirect(reverse("organizer-dashboard") + "#categories")

    return render(request, "category/form.html", {"form": form})


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def category_delete(request, id):
    if request.method == "POST":
        category = Category.objects.get(id=id)
        category.delete()
        messages.success(request, "Category Deleted Successfully")

    return HttpResponseRedirect(reverse("organizer-dashboard") + "#categories")


@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    user_groups = [group.name for group in request.user.groups.all()]

    rsvped = event.participants.filter(id=request.user.id).exists()
    context = {"event": event, "user_groups": user_groups, "rsvped": rsvped}

    return render(request, "events/detail.html", context)


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def event_create(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Added Successfully")
            return redirect("organizer-dashboard")

        else:
            messages.error(request, "Something Went Wrong")

    return render(request, "events/form.html", {"form": form})


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def event_update(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(instance=event)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect("organizer-dashboard")

    return render(request, "events/form.html", {"form": form})


@login_required
@user_passes_test(
    lambda user: is_admin(user) or is_organizer(user), login_url="/no-permission/"
)
def event_delete(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")

    return redirect("dashboard")


@login_required
@user_passes_test(is_participant)
def rsvp_event(request, id):
    event = Event.objects.get(id=id)
    if request.user not in event.participants.all():
        event.participants.add(request.user)
    return redirect("participants-dashboard")
