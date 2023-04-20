# contains that url path patterns for the each projects

from django.urls import path
from . import views

# URL configuration
urlpatterns = [
    path('', views.crime_map_index, name="crime_map_index"),
    path('visual-option/', views.visual_option, name="visual_option"),
]