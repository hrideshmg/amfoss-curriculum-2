from typing import Any
from django.urls import reverse
from todoapp.models import ToDoList, ToDoTask
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from todoapp.forms import DateInputWidget

# Create your views here.


class ToDoListList(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = "todoapp/index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist_list"] = self.request.user.todolist_set.all
        return context


class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = "todoapp/tasklist.html"

    def get_context_data(self) -> dict[str, Any]:
        context = super().get_context_data()
        context["todolist"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["list_id"]
        )
        context["todotasks"] = context["todolist"].todotask_set.all
        return context


class ToDoListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todoapp/listadd.html"

    def get_success_url(self) -> str:
        return reverse("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ToDoListDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["pk"]
        )
        return context

    def get_success_url(self) -> str:
        return reverse("index")


class TaskCreate(LoginRequiredMixin, CreateView):
    model = ToDoTask
    fields = ["title", "description", "due_date", "is_completed", "todo_list"]
    template_name = "todoapp/taskadd.html"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["todo_list"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["list_id"]
        )
        initial["is_completed"] = False
        return initial

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["list_id"]
        )
        return context

    def get_success_url(self) -> str:
        return reverse(
            "list",
            args=[self.request.user.todolist_set.get(id=self.kwargs["list_id"]).id],
        )


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoTask
    template_name = "todoapp/taskupdate.html"
    fields = ["title", "description", "due_date", "is_completed", "todo_list"]

    def get_form(self):
        form = super().get_form()
        form.fields["due_date"].widget = DateInputWidget()
        return form

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["list_id"]
        )
        context["todo"] = context["todolist"].todotask_set.get(id=self.kwargs["pk"])
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["todolist"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["list_id"]
        )
        return initial

    def get_success_url(self) -> str:
        return reverse(
            "list",
            args=[self.request.user.todolist_set.get(id=self.kwargs["list_id"]).id],
        )


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = ToDoTask
    template_name = "todoapp/ToDoTask_confirm_delete.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["todolist"] = get_object_or_404(
            self.request.user.todolist_set, id=self.kwargs["list_id"]
        )
        context["todo"] = context["todolist"].todotask_set.get(id=self.kwargs["pk"])
        return context

    def get_success_url(self) -> str:
        return reverse(
            "list",
            args=[self.request.user.todolist_set.get(id=self.kwargs["list_id"]).id],
        )


class LoginForm(LoginView):
    template_name = "todoapp/login.html"


class LogoutForm(LogoutView):
    template_name = "todoapp/logout.html"


class RegistrationForm(FormView):
    template_name = "todoapp/register.html"
    form_class = UserCreationForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
