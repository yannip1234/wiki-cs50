from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.randompage, name="random"),
    path("edit/<str:entrytitle>", views.edit, name="edit"),
    path("<str:entryname>", views.getentry, name="getentry")

]
