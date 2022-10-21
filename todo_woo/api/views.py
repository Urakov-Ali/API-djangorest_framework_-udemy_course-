from rest_framework import generics, permissions
from todo.models import Todo
from .serializers import TodoListSerializer, TodoCompleteSerializer
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status=400)

@csrf_exempt
def logIn(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse({'error':'Could not log in please check username and password'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
                return JsonResponse({'token':str(token)}, status=200)

class CreateTodoList(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        create = Todo.objects.filter(user=user)
        return create

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoEditList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        todos = Todo.objects.filter(user=user)
        return todos

class CompletedTodoList(generics.ListAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        completed = Todo.objects.filter(user=user, completed_at__isnull=False).order_by('-completed_at')
        return completed

class CompleteTodoList(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        complete = Todo.objects.filter(user=user)
        return complete

    def perform_update(self, serializer):
        serializer.instance.completed_at = timezone.now()
        serializer.save()
