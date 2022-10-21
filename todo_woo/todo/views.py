from urllib import request
from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def indexView(request):
    return render(request, 'index.html')

def userReg(request):
    if request.method == 'GET':
            return render(request, 'user_rigester.html', {'form':UserCreationForm()})
    
    else:
            if request.POST['password1']  == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('currentTodo')
                except IntegrityError:
                    return render(request, 'user_rigester.html', {'form':UserCreationForm(), 'token':'The username is already token, please use another one'})
            else: 
                return render(request, 'user_rigester.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def userLog_in(request):
    if request.method == 'GET':
            return render(request, 'user_log_in.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'user_log_in.html', {'form':AuthenticationForm(), 'error':'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('currentTodo')

@login_required
def userLog_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

@login_required   
def createTodo(request):
    if request.method == 'GET':
        return render(request, 'createTodo.html', {'form': TodoForm()})

    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('index')
        except ValueError:
            return render(request, 'createTodo.html', {'form': TodoForm(), 'error':'Bad data passed in. Please try again :)'})

@login_required
def currentTodo(request):
    todos = Todo.objects.filter(user = request.user, completed_at__isnull=True)
    return render(request, 'currentTodo.html', {'todos':todos})

@login_required
def viewTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'viewTodo.html', {'todo':todo, 'form':form})
    else:
        try: 
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentTodo')
        except ValueError:
            return render(request, 'viewTodo.html', {'todo':todo, 'form':form, 'error':'Bad data passed in. Please try again :)'})

@login_required
def completeTodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed_at = timezone.now()
        todo.save()
        return redirect('currentTodo')

@login_required    
def completedTodo(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user = request.user, completed_at__isnull=False)
        return render(request, 'completed.html', {'todos':todos})

@login_required
def deleteTodo(request, todo_pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=todo_pk, user = request.user)
        todo.delete()
        return redirect('currentTodo')

