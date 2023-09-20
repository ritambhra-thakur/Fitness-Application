from django.urls import path
from rest_framework.routers import DefaultRouter

from pomodoro import views

app_name = "pomodoro"

urlpatterns = [
	path("get/<int:id>/", views.GetPomodoro.as_view()),
    path("list/", views.GetAllPomodoro.as_view()),
    path("update/<int:id>/", views.UpdatePomodoro.as_view()),
    path("create/", views.CreatePomodoro.as_view()),
    path("delete/<int:id>/", views.DeletePomodoro.as_view()),
]
router = DefaultRouter()
urlpatterns += router.urls