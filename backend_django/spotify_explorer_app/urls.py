from django.urls import path, include

from spotify_explorer_app import views

urlpatterns = [
    path('artist/<slug:sp_id>/', views.ArtistDetail.as_view()),
    path('artists/', views.ArtistList.as_view()),
]