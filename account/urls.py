from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegistrationView,UserUpdateView
urlpatterns = [
    path('',UserUpdateView.as_view(),name='account'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
]