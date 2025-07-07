from django.urls import path
from events.views import *

urlpatterns = [
    path("dashboard/", organizer_dashboard, name="organizer-dashboard"),

    path("categories/", category_list, name="category-list"),
    path("categories/create/", category_create, name="category-create"),
    path("categories/edit/<int:id>/", category_update, name="category-update"),
    path("categories/delete/<int:id>/", category_delete, name="category-delete"),

    path("events/", event_list, name="event-list"),
    path("events/<int:id>/", event_detail, name="event-detail"),
    path("events/create/", event_create, name="event-create"),
    path("events/edit/<int:id>/", event_update, name="event-update"),
    path("events/delete/<int:id>/", event_delete, name="event-delete"),

    path("participants/", participant_list, name="participant-list"),
    path("participants/create/", participant_create, name="participant-create"),
    path("participants/edit/<int:id>/", participant_update, name="participant-update"),
    path("participants/delete/<int:id>/", participant_delete, name="participant-delete"),
]
