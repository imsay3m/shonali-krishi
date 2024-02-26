from django.urls import path
from .views import ComingSoonView, home,AboutView
urlpatterns = [
    path('',home,name="home"),
    path('about/',AboutView.as_view(),name="about"),
    path('coming-soon/',ComingSoonView.as_view(),name="coming_soon")
]
