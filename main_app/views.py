# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Comment
from .forms import CommentForm

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
  comment_form = CommentForm()
  return render(request, 'events/detail.html', {
    'event': event,
    'comment_form': comment_form,
  })

# class EventDetail(DetailView):
#   model = Event

def add_comment(request, event_id):
  # create a ModelForm instance using the data in request.POST
  form = CommentForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_comment = form.save(commit=False)
    new_comment.event_id = event_id
    new_comment.user = request.user
    new_comment.save()
  return redirect('detail', event_id=event_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    success_url = '/events'

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = '/events' #maybe add /events back

class EventCreate(LoginRequiredMixin, CreateView):
  model = Event
  fields = ['title', 'datetime', 'description', 'address', 'neighborhood', 'city']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
  model = Event
  fields = ['title', 'datetime', 'description', 'address', 'neighborhood', 'city']

class EventDelete(LoginRequiredMixin, DeleteView):
  model = Event
  success_url = '/events'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)