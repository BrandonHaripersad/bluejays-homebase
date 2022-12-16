from django.urls import path
from . import views

urlpatterns = [
    path("", views.standings, name="standings"),
    path("roster/<str:id>", views.roster, name="roster"),
    path("player/<str:id>", views.player, name="player"),
    path("leaders", views.leaders, name="leaders")
]