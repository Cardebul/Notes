from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('create/', views.NoteCreateView.as_view(), name='create'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(),
         name='detail'),
    path('list/', views.NoteListView.as_view(), name='list'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='edit'),
    path('note/<int:pk>/delete/',
         views.NoteDeleteView.as_view(), name='delete'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

]
