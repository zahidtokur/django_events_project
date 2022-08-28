from django.urls import path
from . import views

urlpatterns = [
    path("", views.EventListView.as_view(), name="home"),
    path("event/create/", views.EventCreateView.as_view(), name="create"),
    path("event/created/", views.EventCreatedListView.as_view(), name="created_list"),
    path("event/joined/", views.EventJoinedListView.as_view(), name="joined_list"),
    path("event/<int:pk>/update/", views.EventUpdateView.as_view(), name="update"),
    path("event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="delete"),
    path("event/<int:pk>/join/", views.EventJoinView.as_view(), name="join"),
    path("event/<int:pk>/unjoin/", views.EventUnjoinView.as_view(), name="unjoin"),
]
