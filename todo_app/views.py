from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import todo_app

from todo_app.models import ToDoItem

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html' 
    fields = '__all__'
    redirect_authenticated_user = True 

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'todo_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = ToDoItem
    context_object_name = 'todo_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = context['todo_list'].filter(user=self.request.user)
        context['count'] = context['todo_list'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['todo_list'] = context['todo_list'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input 
        
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = ToDoItem
    context_object_name = 'todoitem'
    template_name = 'todo_app/todoitem.html' 

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['todoitem'] = context['todoitem'].filter(user=self.request.user)
    #    context['count'] = context['todoitem'].filter(complete=False).count()
    #    return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = ['title', 'description', 'due_date', 'complete', 'todo_list']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = ['title', 'description', 'due_date', 'complete', 'todo_list']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoItem
    context_object_name = 'todoitem'
    success_url = reverse_lazy('tasks')



