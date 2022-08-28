from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import UserOwnsEventMixin
from .forms import EventForm

from .models import Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name_suffix = '_create'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
       form.instance.created_by = self.request.user
       return super().form_valid(form)


class EventUpdateView(UserOwnsEventMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name_suffix = '_update'
    success_url = reverse_lazy("home")


class EventDeleteView(UserOwnsEventMixin, DeleteView):
    model = Event
    template_name_suffix = '_delete'
    success_url = reverse_lazy("home")


class EventListView(ListView):
    model = Event
    ordering = 'date'
    paginate_by = 3

    def get_queryset(self):
        today = timezone.now()
        return super().get_queryset().filter(date__gte=today)

class EventJoinView(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        if self.request.user not in event.guests.all():
            event.guests.add(self.request.user)
        return reverse_lazy('joined_list')


class EventUnjoinView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs['pk'])
        if self.request.user in event.guests.all():
            event.guests.remove(self.request.user)
        return reverse_lazy('joined_list')


class EventCreatedListView(EventListView):

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)


class EventJoinedListView(EventListView):

    def get_queryset(self):
        return super().get_queryset().filter(guests__id=self.request.user.id)

