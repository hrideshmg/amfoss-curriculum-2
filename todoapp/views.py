from typing import Any
from django.urls import reverse
from todoapp.models import ToDoList, ToDoTask
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.


class ToDoListList(ListView):
    model = ToDoList
    template_name = "todoapp/index.html"
    context_object_name = "todolist_list"


class ToDoListView(ListView):
    model = ToDoList
    template_name = "todoapp/tasklist.html"

    def get_context_data(self) -> dict[str, Any]:
        context = super().get_context_data()
        context["todolist"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todotasks"] = context["todolist"].todotask_set.all
        return context


class ToDoListCreate(CreateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todoapp/listadd.html"

    def get_success_url(self) -> str:
        return reverse("index")


class ToDoListDelete(DeleteView):
    model = ToDoList

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = ToDoList.objects.get(id=self.kwargs["pk"])
        return context

    def get_success_url(self) -> str:
        return reverse("index")


class TaskCreate(CreateView):
    model = ToDoTask
    fields = ["title", "description", "due_date", "todo_list"]
    template_name = "todoapp/taskadd.html"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return initial

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

    def get_success_url(self) -> str:
        return reverse(
            "list",
            args=[ToDoList.objects.get(id=self.kwargs["list_id"]).id],
        )


class TaskUpdate(UpdateView):
    model = ToDoTask
    template_name = "todoapp/taskupdate.html"
    fields = ["title", "description", "due_date", "todo_list"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo"] = ToDoTask.objects.get(id=self.kwargs["pk"])
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return initial

    def get_success_url(self) -> str:
        return reverse(
            "list",
            args=[ToDoList.objects.get(id=self.kwargs["list_id"]).id],
        )


class TaskDelete(DeleteView):
    model = ToDoTask
    template_name = "todoapp/ToDoTask_confirm_delete.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todo"] = ToDoTask.objects.get(id=self.kwargs["pk"])
        context["todolist"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

    def get_success_url(self) -> str:
        return reverse(
            "list",
            args=[ToDoList.objects.get(id=self.kwargs["list_id"]).id],
        )
