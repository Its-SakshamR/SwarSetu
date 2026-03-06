from django.urls import path
from . import views

urlpatterns = [
    path("", views.song_list_create),
    path("<int:id>/", views.song_detail),
    path("translate/", views.translate),
]