# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Event

# Define the home view
def home(request):
  return render(request, 'home.html')

# about view
def about(request):
  return render(request, 'about.html')

def events_index(request):
  events = Event.objects.all()
  return render(request, 'events/index.html', {
    'events': events
  })

def events_detail(request, event_id):
  event = Event.objects.get(id=event_id)
  return render(request, 'events/detail.html', {
    'event': event
  })

# class EventDetail(DetailView):
#   model = Event

class EventCreate(CreateView):
  model = Event
  fields = '__all__'

class EventUpdate(UpdateView):
  model = Event
  fields = '__all__'

class EventDelete(DeleteView):
  model = Event
  success_url = '/events'