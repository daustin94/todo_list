# todo_list/todo_app/models.py
from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse 

# Create your models here.
def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse('list', args=[self.id])
    
    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    complete = models.BooleanField(default=False)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title}: due {self.due_date}'

    class Meta:
        ordering = ['complete']
