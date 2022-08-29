from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event
from .forms import EventForm
from .mixins import UserOwnsEventMixin


class EventListView(ListView):
    model = Event
    paginate_by = 5

    def get_queryset(self):
        today = timezone.now()
        objects = self.model.objects.filter(
            date__gte=today).order_by('date')
        return objects.prefetch_related('guests')


class EventCreatedListView(LoginRequiredMixin, EventListView):

    def get_queryset(self):
        today = timezone.now()
        objects = self.request.user.created_events.filter(
            date__gte=today).order_by('date')
        return objects.prefetch_related('guests')


class EventJoinedListView(LoginRequiredMixin, EventListView):

    def get_queryset(self):
        today = timezone.now()
        objects = self.request.user.joined_events.filter(
            date__gte=today).order_by('date')
        return objects.prefetch_related('guests')


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
