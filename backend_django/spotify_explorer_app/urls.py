from django.urls import path
from spotify_explorer_app import views

from .views import *

urlpatterns = [
    path('artist/<slug:sp_id>/', views.ArtistDetail.as_view()),
    path('artists/', views.ArtistList.as_view()),
    path('redirect', spotify_callback),
    path('me/following/', views.UserFollowingList.as_view()),
    path('sp/artist/<slug:sp_id>/', views.SpFetchArtist.as_view()),
    path('sp/artist/<slug:sp_id>/albums', views.SpFetchAlbums.as_view()),
    path('sp/me/following/', views.SpFetchFollowing.as_view()),
    path('sp/logout/', views.SpLogout.as_view()),
    path('sp_is_auth/', views.SpIsAuthenticated.as_view()),
    path('sp_get_auth_url/', views.SpGetAuthURL.as_view()),
]
