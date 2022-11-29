from django.db import models
from django.urls import reverse
from datetime import date
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg

CITIES = (
    ('Seattle', 'Seattle'),
    ('Los Angeles', 'Los Angeles'),
    ('San Francisco', 'San Francisco')
)

NEIGHBORHOODS = (
  ('SEATTLE NEIGBORHOODS, CHOOSE ONE', 'SEATTLE NEIGBORHOODS, CHOOSE ONE BELOW'),
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
  ('Eastlake', 'Eastlake'),
  ('SAN FRANCISCO NEIGBORHOODS, CHOOSE ONE', 'SAN FRANCISO NEIGBORHOODS, CHOOSE ONE BELOW'),
  ('Sunset', 'Sunset' ),
  ('Richmond', 'Richmond'),
  ('Ingleside', 'Ingleside'),
  ('Haight', 'Haight'),
  ('Presidio', 'Presidio'),
  ('Mission', 'Mission'),
  ('Pacific Heights', 'Pacific Heights'),
  ('Portola', 'Portola'),
  ('Castro', 'Castro'),
  ('Nob Hill', 'Nob Hill'),
  ('South of Market', 'South of Market'),
  ('Noe Valley', 'Noe Valley'),
  ('LOS ANGELES NEIGBORHOODS, CHOOSE ONE', 'LOS ANGELES NEIGBORHOODS, CHOOSE ONE BELOW'),
  ('Hollywood', 'Hollywood'),
  ('Downtown LA', 'Downtown LA'),
  ('Venice', 'Venice'),
  ('Koreatown', 'Koreatown'),
  ('North Hollywood', 'North Hollywood'),
  ('Brentwood', 'Brentwood'),
  ('Sherman Oaks', 'Sherman Oaks'),
  ('Echo Park', 'Echo Park'),
  ('Encino', 'Encino'),
  ('Beverly Hills', 'Beverly Hills'),
  ('Los Feliz', 'Los Feliz'),
  ('Hollywood Hills', 'Hollywood Hills'),
  ('Leimert Park', 'Leimert Park'),
  ('Larchmont Village', 'Larchmont Village'),
  ('West Hollywood', 'West Hollywood'),
  ('East Hollywood', 'East Hollywood'),
  ('Silver Lake', 'Silver Lake'),
  ('Santa Monica', 'Santa Monica'),
)



class Event(models.Model):
  title = models.CharField(max_length=40)
  date = models.DateField(validators=[MinValueValidator(date.today)])
  time = models.TimeField('Time', default='12:00')
  description = models.TextField(max_length=1500)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length= 30, choices=CITIES, default='Seattle')
  neighborhood = models.CharField(max_length=50, choices=NEIGHBORHOODS, default='Queen Anne')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def average_rating(self) -> float:
    return Rating.objects.filter(event=self).aggregate(Avg("rating"))["rating__avg"] or 0

  def __str__(self):
    return f'{self.title} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'event_id': self.id})

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
      return f"{self.event.title}: {self.rating}"
  
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