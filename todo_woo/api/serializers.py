from rest_framework import serializers
from todo.models import Todo

class TodoListSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'memo', 'created_at', 'important']

class TodoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id',]
        read_only_fields = ['user', 'title', 'memo', 'created_at', 'important']
