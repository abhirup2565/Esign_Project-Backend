from django.urls import path
from .views import UserCreateView,UserListView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("list/", UserListView.as_view(), name="user_list"),
]