from curses.ascii import US
from challenge import serializers
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from rest_framework.permissions import AllowAny, IsAuthenticated
import django_filters
from django_filters import rest_framework as filters
from todo.models import Todo
from todo.serializers import ToDoCreateSerializer, ToDoGetSerializer
from rest_framework import permissions
from utils.saveTaskCompletionDetails import save_completion_details


from users.models import User

class ToDoViewSets(viewsets.ModelViewSet):
    serializer_class = ToDoCreateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Todo.objects.filter(owner=self.request.user)
        return queryset

class testView(APIView):
    def post(self, request, format=None):
        
        date = request.data.get('date')
        current_time = request.data.get('current_time')
        
        if date is None:
            todo = Todo.objects.filter(owner = request.user.id)
        else: 
            if current_time is None:
                return Response({"data":None, "message":"Please Specify Time", "status":400}, status = 400)
            todo = Todo.objects.filter(due_date = date, owner = request.user.id)
            

        context = {"current_time":current_time}
        serializer = ToDoGetSerializer(todo, many=True, context = context)
        return Response({"data":serializer.data, "message":"Data Fetched Successfully", "status":200}, status = 200)

class DeleteAlltodo(APIView):
    queryset = Todo.objects.all()
    serializer = ToDoCreateSerializer

    def delete(self, request, owner):
        try:
            user_obj = User.objects.get(id = owner)
        except User.DoesNotExist:
            return Response({"message":"Owner Does not Exist!", "status":400}, status = 400)        
        todo_obj = Todo.objects.filter(owner = owner).delete()
        return Response({"message":"Data Deleted Successfully", "status":200}, status = 200)

class UpdateTodoView(APIView):

    def patch(self, request, id):
        try:
            todo_obj = Todo.objects.get(id = id)
        except User.DoesNotExist:
            return Response({"message":"Todo Does not Exist!", "status":400}, status = 400)        

        serializer = ToDoCreateSerializer(todo_obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            if 'is_completed' in request.data and request.data['is_completed'] is True:
                try:
                    a = save_completion_details(1, serializer.data['id'], user_id = request.user.id)
                except:
                    pass
            data = serializer.data
            data['message'] = "Todo Updated Successfully"
            data['status'] = 200
            return Response(data, status = 200)
        else:
            return Response({"message":serializer.errors, "status":400}, status = 400)