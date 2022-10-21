from django.urls import path
from .views import CompletedTodoList, CreateTodoList, TodoEditList,  CompleteTodoList, signUp, logIn

urlpatterns = [
    path('todos/<int:pk>',TodoEditList.as_view()),
    path('todos/<int:pk>/complete', CompleteTodoList.as_view()),
    path('todos/completed',CompletedTodoList.as_view()),
    path('todos/create',CreateTodoList.as_view()),

    #auth
    path('todos/signup', signUp),
    path('todos/login', logIn),

]
