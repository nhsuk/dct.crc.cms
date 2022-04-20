from django.contrib.auth.models import User
from django.urls import path

from .admin_views import index, edit, set_password


app_name = "paragon_users"

urlpatterns = [
    path("", index, name="index"),
    path("edit/<str:user_token>/", edit, name="edit"),
    path("set_password/<str:user_token>/", set_password, name="set_password"),
]
