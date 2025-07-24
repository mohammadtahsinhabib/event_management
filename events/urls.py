from django.urls import path
from events.views import *


urlpatterns = [
    # Dashboard Redirect URL
    path("dashboard/", dashboard_redirect, name="dashboard"),
    # User URL
    path("sign-up/", sign_up, name="sign-up"),
    path("sign-in/", sign_in, name="sign-in"),
    path("sign-out/", sign_out, name="sign-out"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    # Admin URL
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin/change-role/<int:user_id>/", change_user_role, name="change-role"),
    path("admin/delete-user/<int:user_id>/", delete_user, name="delete-user"),
    path("admin/create-group/", create_group, name="create-group"),
    path("admin/delete-group/<int:group_id>/", delete_group, name="delete-group"),
    # Organizer URL
    path("organizer-dashboard/", organizer_dashboard, name="organizer-dashboard"),
    path("organizer/event/create/", event_create, name="event-create"),
    path("organizer/event/update/<int:id>/", event_update, name="event-update"),
    path("organizer/event/delete/<int:id>/", event_delete, name="event-delete"),
    path("organizer/categories/create/", category_create, name="category-create"),
    path(
        "organizer/categories/edit/<int:id>/", category_update, name="category-update"
    ),
    path(
        "organizer/categories/delete/<int:id>/", category_delete, name="category-delete"
    ),
    # Participant URL
    path("event/<int:id>/rsvp/", rsvp_event, name="rsvp-event"),
    path(
        "participants-dashboard/", participants_dashboard, name="participants-dashboard"
    ),
    path("events/<int:id>/", event_detail, name="event-detail"),
    path("events/view-events/", view_events, name="view-events"),
]
