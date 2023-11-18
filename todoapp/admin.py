from django.contrib import admin
from todoapp.models import ToDoList, ToDoTask

# Register your models here.
admin.site.register([ToDoTask, ToDoList])
