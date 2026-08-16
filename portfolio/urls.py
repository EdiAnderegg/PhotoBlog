from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path(
        "collections/<slug:slug>/",
        views.CollectionDetailView.as_view(),
        name="collection-detail",
    ),
    path(
        "collections/<slug:collection_slug>/photos/<int:pk>/",
        views.PhotoDetailView.as_view(),
        name="photo-detail",
    ),
]
