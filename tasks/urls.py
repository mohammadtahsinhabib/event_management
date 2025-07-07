from django.urls import path
from tasks.views import *


urlpatterns = [
    path("admin-dashboard/",manager_dashboard,name="manager-dashboard"),
    path("user-dashboard/",user_dashboard),
    path("create-task/",create_task,name="create-task"),
    path("update-task/<int:id>/",update_task,name="update-task"),
    path("view-task/",view_task),
    path("delete-task/<int:id>/",delete_task,name="delete-task"),
    path("footer/",footer),

]
