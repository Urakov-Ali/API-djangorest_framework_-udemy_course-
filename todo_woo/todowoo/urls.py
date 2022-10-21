"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('admin/', admin.site.urls),

    #auth
    path('user/', views.userReg, name='reg'),
    path('login/', views.userLog_in, name='log_in'),
    path('logout/', views.userLog_out, name='log_out'),

    #todos
    path('createTodo/', views.createTodo, name='createTodo'),
    path('currentTodo', views.currentTodo, name='currentTodo'),
    path('Todo/<int:todo_pk>', views.viewTodo, name='viewTodo'),
    path('Todo/<int:todo_pk>/complete>', views.completeTodo, name='completeTodo'),
    path('Todo/completed', views.completedTodo, name='completedTodo'),
    path('Todo/<int:todo_pk>/delete>', views.deleteTodo, name='deleteTodo'),

    #API
    path('api/', include('api.urls'))
]
