from django.urls import path
from .views import CustomTokenObtainPairView,UserCreateView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
]