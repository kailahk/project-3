from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('events/', views.events_index, name='index'),
  path('events/create/', views.EventCreate.as_view(), name='events_create'),
  path('events/<int:event_id>/', views.events_detail, name='detail'),
  path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
  path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
  path('accounts/signup/', views.signup, name='signup'),
  path('events/<int:event_id>/add_comment/', views.add_comment, name='add_comment'),
  path('events/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
  path('events/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
]
