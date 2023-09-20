from django.urls import path
from rest_framework.routers import DefaultRouter

from todo import views

app_name = "todo"

urlpatterns = [
	path("fetch-todo-by-date/", views.testView.as_view()),
	path("delete-all-todo/<int:owner>/",views.DeleteAlltodo.as_view()),
	path("update/<int:id>/",views.UpdateTodoView.as_view()),
]

router = DefaultRouter()

router.register(r'todo', views.ToDoViewSets, basename='todo')


urlpatterns += router.urls