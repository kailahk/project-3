from django.db import models
from django.urls import reverse
# from datetime import date
from django.contrib.auth.models import User

CITIES = (
    ('Seattle', 'Seattle'),
    ('Los Angeles', 'Los Angeles'),
    ('San Francisco', 'San Francisco')
)

NEIGHBORHOODS = (
  ('Queen Anne', 'Queen Anne'),
  ('Capitol Hill', 'Capitol Hill'),
  ('Downtown', 'Downtown'),
  ('Belltown', 'Belltown'),
  ('West Seattle', 'West Seattle'),
  ('Ballard', 'Ballard'),
  ('Fremont', 'Fremont'),
  ('South Lake Union', 'South Lake Union'),
  ('University District', 'University District'),
  ('Pioneer Square', 'Pioneer Square'),
  ('International District', 'International District'),
  ('Eastlake', 'Eastlake')
)


class Event(models.Model):
  title = models.CharField(max_length=40)
  date = models.DateField('Date', default='2023-01-01')
  time = models.TimeField('Time', default='12:00')
  description = models.TextField(max_length=1500)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length= 30, choices=CITIES, default='Seattle')
  neighborhood = models.CharField(max_length=50, choices=NEIGHBORHOODS, default='Queen Anne')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)


  def __str__(self):
    return f'{self.title} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'event_id': self.id})
  
class Comment(models.Model):
  content = models.CharField(max_length=150)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE) 

  def __str__(self):
    return f"{self.content}"

  class Meta:
    ordering = ['-created_at']

  # def get_absolute_url(self):
  #   print(self.event, 'testing')
  #   return reverse('detail', kwargs={'event_id': self.event})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"