from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from drf_yasg import openapi
from .models import Pomodoro
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from .serializers import GetPomodoroSerializer, PomodoroSerializer
from utils.fetchSerializerErrors import fetch_serializer_error
from utils.saveTaskCompletionDetails import save_completion_details
from utils.checkUserSubscription import check_user_subscription



class GetPomodoro(APIView):

    def get(self, request, id, format=None):
        if id:
            item = Pomodoro.objects.get(id=id)
            print(item)
            serializer = GetPomodoroSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Pomodoro.objects.all()
        serializer = GetPomodoroSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetAllPomodoro(APIView):

    queryset = Pomodoro.objects.all()


    owner_id = openapi.Parameter(
        "owner_id",
        in_=openapi.IN_QUERY,
        description="owner_id",
        type=openapi.TYPE_STRING,
    )


    date = openapi.Parameter(
        "date",
        in_=openapi.IN_QUERY,
        description="date",
        type=openapi.TYPE_STRING,
    )

    search_text = openapi.Parameter(
        "search_text",
        in_=openapi.IN_QUERY,
        description="search_text",
        type=openapi.TYPE_STRING,
    )

    """Decorator with parameter swagger auto schema"""

    @swagger_auto_schema(manual_parameters=[owner_id, date, search_text])
    @csrf_exempt
    def post(self, request):
        data = request.data
        if 'owner_id' not in data:
            return Response({"data":None, "message":"Please specify Owner ID", "status":400}, status=400) 

        if 'date' in data and data['date'] != "":
            pomodoro_obj = Pomodoro.objects.filter(create_date = data['date'], user = data['owner_id'])
        else:
            pomodoro_obj = Pomodoro.objects.filter(user = data['owner_id'])

        if 'search_text' in data and data["search_text"] != "":
            pomodoro_obj  = pomodoro_obj.filter(name__icontains = data['search_text'])

        final_result = {}
        complete_pomodoro_obj = pomodoro_obj.filter(completed = True).order_by('-id')
        active_pomodoro_obj = pomodoro_obj.filter(completed = False).order_by('-id')


        final_result['completed'] = GetPomodoroSerializer(complete_pomodoro_obj, many=True).data
        final_result['active'] = GetPomodoroSerializer(active_pomodoro_obj, many=True).data

        return Response({"data":final_result, "message":"Pomodoro Fetched Successfully", "status":200}, status=200)
    


class CreatePomodoro(APIView):

    @swagger_auto_schema(
        operation_description="Pomodoro Create API",
        operation_summary="Pomodoro Create API",
        request_body=PomodoroSerializer,
    )
    def post(self, request, format=None):
        data = request.data
        try:
            pomo_obj = Pomodoro.objects.get(user = data['user'], name = data['name'])
            return Response({"data":None, "message": "Pomodoro with this name already exists!", "status":200}, status=200)
        except:
            pass
        serializer = PomodoroSerializer(data=data)

        if serializer.is_valid():
            check_resp = check_user_subscription(request, 2)
            if check_resp['result'] is True:
                serializer.save()
                return Response({"data":serializer.data, "message":"Pomodoro Created Successfully", "status":200}, status=200)
            else:
                return Response({"data":None, "message":check_resp['detail'], "status":400}, status=400)
        else:
            error_message = fetch_serializer_error(serializer.errors)
            return Response({"data":None, "message": error_message, "status":400}, status=400)

            


class UpdatePomodoro(APIView):
    @swagger_auto_schema(
        operation_description="Pomodoro Update API",
        operation_summary="Pomodoro Update API",
        request_body=PomodoroSerializer,
    )
    def put(self, request, id=None, format=None):   

        response = Response()
        try:
            todo_to_update = Pomodoro.objects.get(id=id)
        except Pomodoro.DoesNotExist:

            return Response({"data":None, "message":"Pomodoro not found.", "status":400}, status=400)
        serializer = PomodoroSerializer(instance=todo_to_update,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            try:
                if 'completed' in request.data and request.data['completed'] is True:
                    save_completion_details(task_type = 2, task_id = id, user_id = request.user.id)
            except:
                pass
            return Response({"data":serializer.data, "message":"Pomodoro Updated Successfully.", "status":200}, status=200)
        else:
            error_message = fetch_serializer_error(serializer.errors)
            return Response({"data":None, "message": error_message, "status":400}, status=400)
class DeletePomodoro(APIView):

    def delete(self, request, id, format=None):
        try:
            todo_to_delete =  Pomodoro.objects.get(id=id)
        except Pomodoro.DoesNotExist:
            return Response({"data":None, "message":"Pomodoro not found.", "status":400}, status=400)

        todo_to_delete.delete()
        return Response({"data":None, "message":"Pomodoro Deleted Successfully.", "status":200}, status=200)

