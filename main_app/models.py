from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Event(models.Model):
  title = models.CharField(max_length=40)
  datetime = models.DateField('Date')
  description = models.TextField(max_length=1500)
  address = models.CharField(max_length=100)
  neighborhood = models.CharField(max_length=50)
  city = models.CharField(max_length= 30)
  # comments = models.ManyToManyField(Comment)
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