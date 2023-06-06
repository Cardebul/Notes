from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import NoteForm
from .models import Note, User


class HomeView(TemplateView):
    template_name = 'notes/home.html'


class AboutView(TemplateView):
    template_name = 'notes/about.html'


class RulesView(TemplateView):
    template_name = 'notes/rules.html'


class BaseView(LoginRequiredMixin):
    model = Note

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class NoteCreateView(BaseView, CreateView):
    form_class = NoteForm
    template_name = 'notes/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('notes:list')


class NoteDetailView(BaseView, DetailView):
    template_name = 'notes/detail.html'


class NoteListView(BaseView, ListView):
    template_name = 'notes/list.html'


class NoteUpdateView(BaseView, UpdateView):
    form_class = NoteForm
    template_name = 'notes/create.html'

    def get_success_url(self):
        return reverse_lazy('notes:detail', args=(self.kwargs['pk'],))


class NoteDeleteView(BaseView, DeleteView):
    template_name = 'notes/create.html'
    success_url = reverse_lazy('notes:list')


class ProfileView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'notes/profile.html'

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])

    def dispatch(self, request, *args, **kwargs):
        auth = request.user.is_authenticated
        if request.user.username != kwargs['username'] and auth:
            return redirect('notes:home')
        return super().dispatch(request, *args, **kwargs)
