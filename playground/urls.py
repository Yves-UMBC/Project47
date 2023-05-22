# contains that url path patterns for the each projects

from django.urls import path
from . import views

# URL configuration
urlpatterns = [
    path('', views.crime_map_index, name="crime_map_index"),
    path('visual-option/', views.visual_option, name="visual_option"),
    path('get_crime_data/', views.get_crime_data, name="get_crime_data"),
    path('get_neighborhood_data/', views.get_neighborhood_data, name="get_neighborhood_data"),
    path('delete_chart/', views.delete_chart, name="delete_chart"),
]