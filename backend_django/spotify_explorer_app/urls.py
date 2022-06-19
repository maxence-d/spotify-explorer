from django.urls import path, include

from spotify_explorer_app import views
from .views import *

urlpatterns = [
    path('artist/<slug:sp_id>/', views.ArtistDetail.as_view()),
    path('artists/', views.ArtistList.as_view()),
    path('sp_is_auth/', views.SpIsAuthenticated.as_view()),
    path('sp_get_auth_url/', views.SpGetAuthURL.as_view()),
    path('redirect', spotify_callback),
]