# Create your views here.
import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, Comment, Photo, Rating
from .forms import CommentForm
from datetime import date

# Define the home view
def home(request):
  return render(request, 'home.html')

# about view
def about(request):
  return render(request, 'about.html')

@login_required
def events_index(request):
  events = Event.objects.all()
  today = date.today
  for event in events:
    rating = Rating.objects.filter(event=event, user=request.user).first()
    event.user_rating = rating.rating if rating else 0
  return render(request, 'events/index.html', {
    'events': events,
    'today': today
  })

@login_required
def rate(request, event_id):
    event = Event.objects.get(id=event_id)
    Rating.objects.filter(event=event_id, user=request.user).delete()
    r = Rating(user=request.user, rating=request.POST['rating'], event=event)
    r.save()
    return redirect('detail', event_id = event_id)

@login_required
def events_detail(request, event_id):
  event = Event.objects.get(id=event_id)
  today = date.today 
  comment_form = CommentForm()
  return render(request, 'events/detail.html', {
    'event': event,
    'comment_form': comment_form,
    'today': today
  })

@login_required
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
    def get_success_url(self):
      return f"/events/{self.object.event.id}"

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    def get_success_url(self):
      return f"/events/{self.object.event.id}"

class EventCreate(LoginRequiredMixin, CreateView):
  model = Event
  fields = ['title', 'date', 'time', 'description', 'address', 'city', 'neighborhood']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
  model = Event
  fields = ['title', 'date', 'time', 'description', 'address', 'neighborhood', 'city']

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

@login_required
def events_my_index(request):
  events = Event.objects.filter(user=request.user)
  today = date.today
  return render(request, 'events/my_index.html', {
    'events': events,
    'today': today
  })

def events_seattle(request):
  events = Event.objects.filter(city='Seattle')
  today = date.today
  return render(request, 'events/events_seattle.html', {
    'events': events,
    'today': today
  })

def events_losangeles(request):
  events = Event.objects.filter(city='Los Angeles')
  today = date.today
  return render(request, 'events/events_losangeles.html', {
    'events': events,
    'today': today
  })

def events_sanfrancisco(request):
  events = Event.objects.filter(city='San Francisco')
  today = date.today
  return render(request, 'events/events_sanfrancisco.html', {
    'events': events,
    'today': today
  })

def add_photo(request, event_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, event_id=event_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', event_id=event_id)