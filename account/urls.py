from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegistrationView,user_update_view
urlpatterns = [
    path('',user_update_view,name='account'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
]