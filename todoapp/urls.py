from django.urls import path
from todoapp import views

urlpatterns = [
    path("login/", views.LoginForm.as_view(), name="login"),
    path("register/", views.RegistrationForm.as_view(), name="register"),
    path("logout/", views.LogoutForm.as_view(), name="logout"),
    path("", views.ToDoListList.as_view(), name="index"),
    path("list/<int:list_id>", views.ToDoListView.as_view(), name="list"),
    path("list/add", views.ToDoListCreate.as_view(), name="list-add"),
    path("list/delete/<int:pk>", views.ToDoListDelete.as_view(), name="list-delete"),
    path("list/<int:list_id>/add/", views.TaskCreate.as_view(), name="task-add"),
    path(
        "list/<int:list_id>/update/<int:pk>/",
        views.TaskUpdate.as_view(),
        name="task-update",
    ),
    path(
        "list/<int:list_id>/delete/<int:pk>/",
        views.TaskDelete.as_view(),
        name="todo-delete",
    ),
]
