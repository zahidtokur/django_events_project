from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date']
    template_name_suffix = '_create'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
       form.instance.created_by = self.request.user
       return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date']
    template_name_suffix = '_update'
    success_url = reverse_lazy("home")


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name_suffix = '_delete'
    success_url = reverse_lazy("home")


class EventListView(ListView):
    model = Event


class EventToggleJoinView(DetailView):
    model = Event

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user in self.object.guests.all():
            self.object.guests.remove(request.user)
        else:
            self.object.guests.add(request.user)
        return super().get(request, *args, **kwargs)


class EventCreatedListView(ListView):
    model = Event


class EventJoinedListView(ListView):
    model = Event