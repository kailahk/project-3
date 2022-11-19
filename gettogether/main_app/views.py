# Create your views here.
from django.shortcuts import render
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