from django.db import models
from django.urls import reverse
from django.utils import timezone


class ToDoList(models.Model):
    title = models.CharField(max_length=120, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class ToDoTask(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    created_date = models.DateField(
        auto_now_add=True
    )  # Auto_now_add adds the timestamp on object creation
    due_date = models.DateTimeField()
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("task-update", args=[self.todo_list.id, self.id])

    def __str__(self):
        return self.title
