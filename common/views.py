import code
from challenge.serializers import FriendChallengeCreateSerializer
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.conf import settings
from pomodoro.models import *
from challenge.models import *

from rest_framework.permissions import AllowAny, IsAuthenticated
import django_filters
from django_filters import rest_framework as filters
from todo.models import Todo
from common.models import  *
from rest_framework.parsers import MultiPartParser
from challenge.models import *
from todo.serializers import ToDoCreateSerializer, ToDoGetSerializer
from challenge.serializers import GetFriendChallengeSerializer
from pomodoro.serializers import *
from users import management
from challenge.serializers import GetCompletionDetailsSerializer
from users.models import User
from common.models import Category

from common.serializers import *
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from django.db.models import Q, F
from utils.fetchSerializerErrors import fetch_serializer_error
from datetime import datetime


class TagsViewSets(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Tags.objects.filter(owner=self.request.user)
        return queryset


class EmojiViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'head', 'options', 'trace']	
    serializer_class = EmojiSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Emoji.objects.all()
        return queryset




class TimeLineViewSets(viewsets.ModelViewSet):
    http_method_names = ['get', 'head', 'options', 'trace']	
    serializer_class = TimelineSerializer

    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = Timeline.objects.all()
        return queryset

class GetTimeline(APIView):

    def get(self, request, id, format=None):
        if id:
            item = Timeline.objects.get(id=id)
            print(item)
            serializer = TimelineSerializer(item)
            return Response({"data":serializer.data, "message":"Timeline Fetched Successfully.", "status":200}, status=200)
        
        items = Timeline.objects.all()
        serializer = TimelineSerializer(items, many=True)
        return Response({"data":serializer.data, "message":"Timeline Fetched Successfully.", "status":200}, status=200)


class GetAllTimeline(APIView):

    queryset = Timeline.objects.all()


    """Decorator with parameter swagger auto schema"""

    @csrf_exempt
    def get(self, request):
        
        timeline_obj = Timeline.objects.filter(user = request.user.id)
        
        serializer = TimelineSerializer(timeline_obj, many=True)
        return Response({"data":serializer.data, "message":"Timeline Fetched Successfully", "status":200}, status=200)
    


class CreateTimeline(APIView):

    @swagger_auto_schema(
        operation_description="Timeline Create API",
        operation_summary="Timeline Create API",
        request_body=TimelineSerializer,
    )
    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id
        check_existing = Timeline.objects.filter(user = data['user'], number_of_days = data['number_of_days'])
        if check_existing.count() > 0:
            return Response({"data":None, "message":"Timeline with Number of Days Already Exists!", "status":400}, status=400)
        serializer = TimelineSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)


class UpdateTimeline(APIView):
    @swagger_auto_schema(
        operation_description="Timeline Update API",
        operation_summary="Timeline Update API",
        request_body=TimelineSerializer,
    )
    def put(self, request, id=None, format=None):   
        print(request.data)
        response = Response()
        try:
            todo_to_update = Timeline.objects.get(id=id)
        except Timeline.DoesNotExist:
            return Response({"data":None, "message":"Timeline Does not Exist", "status":400}, status=400)
        serializer = TimelineSerializer(instance=todo_to_update,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()        

        response.data = {
            'message': 'Timeline Updated Successfully',
            'data': serializer.data
        }

        return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
class DeleteTimeline(APIView):

    def delete(self, request, id, format=None):
        try:
            todo_to_delete =  Timeline.objects.get(id=id)
        except Timeline.DoesNotExist:
            return Response({"data":None, "message":"Timeline Does not Exist!", "status":400}, status=400)

        todo_to_delete.delete()

        return Response({"data":None, "message":"Timeline Deleted Successfully", "status":200}, status=200)


class GetCategory(APIView):

    def get(self, request, id, format=None):
        if id:
            item = Category.objects.get(id=id)
            print(item)
            serializer = CategorySerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Category.objects.all()
        serializer = CategorySerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class GetAllCategory(APIView):

    queryset = Category.objects.all()
    name = openapi.Parameter(
        "name",
        in_=openapi.IN_QUERY,
        description="name",
        type=openapi.TYPE_STRING,
    )

    """Decorator with parameter swagger auto schema"""

    @swagger_auto_schema(manual_parameters=[ name])
    @csrf_exempt
    def post(self, request):
        category_obj = Category.objects.filter(Q(user = request.user.id) | Q(default = True)).order_by('-id')
        serializer = GetCategorySerializer(category_obj, many=True)
        return Response({"data":serializer.data, "message":"Category Fetched Successfully", "status":200}, status=200)
    


class CreateCategory(APIView):
    # parser_classes = [MultiPartParser]


    @swagger_auto_schema(
        operation_description="Category Create API",
        operation_summary="Category Create API",
        request_body=CategorySerializer
    )
    def post(self, request, format=None):
        print('--------------------->>>')
        data = request.data
        data['user'] = request.user.id
        serializer = CategorySerializer(
            data=data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)


class UpdateCategory(APIView):
    @swagger_auto_schema(
        operation_description="Category Update API",
        operation_summary="Category Update API",
        request_body=CategorySerializer,
    )
    def put(self, request, id=None, format=None):   
        print(request.data)
        response = Response()
        try:
            todo_to_update = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({"data":None, "message":"Category Does not Exist", "status":400}, status=400)
        serializer = CategorySerializer(instance=todo_to_update,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()        

        response.data = {
            'message': 'Category Updated Successfully',
            'data': serializer.data
        }

        return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
class DeleteCategory(APIView):

    def delete(self, request, id, format=None):
        try:
            todo_to_delete =  Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({"data":None, "message":"Category Does not Exist!", "status":400}, status=400)


        todo_to_delete.delete()

        return Response({"data":None, "message":"Category Deleted Successfully", "status":200}, status=200)

class GetType(APIView):

    def get(self, request, id=None):
        if id:
            item = Type.objects.get(id=id)
            serializer = TypeSerializer(item)
            return Response({"status": "Get Type", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Type.objects.all()
        serializer = TypeSerializer(items, many=True)
        return Response({"status": "Get Type", "data": serializer.data}, status=status.HTTP_200_OK)

class GetAllType(APIView):

    queryset = Type.objects.all()
    user = openapi.Parameter(
        "user",
        in_=openapi.IN_QUERY,
        description="user",
        type=openapi.TYPE_STRING,
    )

    category = openapi.Parameter(
        "category",
        in_=openapi.IN_QUERY,
        description="category",
        type=openapi.TYPE_STRING,
    )

    """Decorator with parameter swagger auto schema"""

    @swagger_auto_schema(manual_parameters=[user, category])
    @csrf_exempt
    def post(self, request):
        data = request.data
        if 'category' in data:
            try:
                category_obj = Category.objects.get(id = data['category'])
            except:
                return Response({"data":None, "message":"Category Does not Exist!", "status":400}, status=400)
            if category_obj.default is True:
                type_obj = Type.objects.filter(category = data['category'])
            else:
                type_obj = Type.objects.filter(user = request.user.id, category = data['category'])
            
            
        else:
            type_obj = Type.objects.filter(Q(user = request.user.id) | Q(default = True))

        serializer = GetTypeSerializer(type_obj, many=True)
        return Response({"data":serializer.data, "message":"Type Fetched Successfully", "status":200}, status=200)

class GetAllUnitsView(APIView):

    # @swagger_auto_schema(manual_parameters=[user, category])
    @csrf_exempt
    def get(self, request):

        category_obj = Units.objects.filter(is_active = True)    
        serializer = GetUnitsSerializer(category_obj, many=True)
        return Response({"data":serializer.data, "message":"Units Fetched Successfully", "status":200}, status=200)

class GetAllCategoryEmojiView(APIView):

    # @swagger_auto_schema(manual_parameters=[user, category])
    @csrf_exempt
    def get(self, request):
        category_emoji_obj = CategoryEmoji.objects.filter(is_active = True)    
        serializer = GetCategoryEmojiSerializer(category_emoji_obj, many=True)
        return Response({"data":serializer.data, "message":"Units Fetched Successfully", "status":200}, status=200)

class GetAllMessageEmojiView(APIView):

    # @swagger_auto_schema(manual_parameters=[user, category])
    @csrf_exempt
    def get(self, request):
        category_emoji_obj = MessageEmoji.objects.filter(is_active = True)
        serializer = GetMessageEmojiSerializer(category_emoji_obj, many=True)
        return Response({"data":serializer.data, "message":"Message Emoji Fetched Successfully.", "status":200}, status=200)

class GetAllTypeEmojiView(APIView):

    # @swagger_auto_schema(manual_parameters=[user, category])
    @csrf_exempt
    def get(self, request):
        type_emoji_obj = TypeEmoji.objects.filter(is_active = True)    
        serializer = GetTypeEmojiSerializer(type_emoji_obj, many=True)
        return Response({"data":serializer.data, "message":"Units Fetched Successfully", "status":200}, status=200)
class CreateType(APIView):
    # parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Type Create API",
        operation_summary="Type Create API",
        request_body=TypeSerializer,
    )
    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id
        serializer = TypeSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)

class GlobalSearchView(APIView):

    def get(self, request, search_text, format=None): 
        current_time = request.GET.get('current_time')
        context = {"request":request, "current_time":current_time}
        pomodoro = GetPomodoroSerializer(Pomodoro.objects.filter(name__icontains = search_text, user = request.user.id), many=True, context = context).data
        self_challenge = GetFriendChallengeSerializer(FriendChallenge.objects.filter(name__icontains = search_text, owner = request.user.id, challenger = request.user.id), many=True, context = context).data
        friend_challenge =  GetFriendChallengeSerializer(FriendChallenge.objects.filter(~Q(owner=F('challenger')), owner = request.user.id, name__icontains = search_text), many=True, context = context).data
        todo = ToDoGetSerializer(Todo.objects.filter(name__icontains = search_text, owner = request.user.id), many=True, context = context).data

        response_data = {
            "pomodoro":pomodoro,
            "self_challenge":self_challenge,
            "friend_challenge":friend_challenge,
            "todo":todo
        }

        return Response({"data":response_data, "message":"Search Data Fetched Successfully.", "status":200}, status=200)


class HomePageView(APIView):

    def get(self, request, format=None):
        current_time = request.GET.get('current_time')
        context = {"request":request, "current_time":current_time}
        all_completed_events = CompletionDetails.objects.filter(owner = request.user.id)

        completed_self_challenges = all_completed_events.filter(self_challenge__isnull=False).values_list('self_challenge', flat=True)
        completed_friend_challenges = all_completed_events.filter(friend_challenge__isnull=False).values_list('friend_challenge', flat=True)
        print('--------------------------------------- completed_self_challenges')
        print(completed_self_challenges)
        print('--------------------------------------- completed_friend_challenges')
        print(completed_friend_challenges)

        self_challenge = {
            "on_going": GetFriendChallengeSerializer(FriendChallenge.objects.filter(owner = request.user.id, challenger = request.user.id, start_date__lte = datetime.now().date()).exclude(id__in = completed_self_challenges), many=True, context = context).data,
            "up_coming": GetFriendChallengeSerializer(FriendChallenge.objects.filter(owner = request.user.id, challenger = request.user.id, start_date__gt = datetime.now().date()).exclude(id__in = completed_self_challenges), many=True, context = context).data
        }

        friend_challenge = {
            "on_going": GetFriendChallengeSerializer(FriendChallenge.objects.filter(~Q(owner=F('challenger')), owner = request.user.id, start_date__lte = datetime.now().date()).exclude(id__in = completed_friend_challenges), many=True, context = context).data,
            "up_coming": GetFriendChallengeSerializer(FriendChallenge.objects.filter(~Q(owner=F('challenger')), owner = request.user.id, start_date__gt = datetime.now().date()).exclude(id__in = completed_friend_challenges), many=True, context = context).data
        }

        #fetching Todo with Urgent Tag
        
        todo_obj = Todo.objects.filter(owner = request.user.id, due_date__gte = datetime.now().date()).exclude(is_completed = True)
        urgent_todo = []
        urgent_todo_ids = []
        for todo in todo_obj:
            if 'Urgent' in list(todo.tags.values_list('name', flat=True)):
                urgent_todo.append(todo)
                urgent_todo_ids.append(todo.id)
        
        due_todo = list(Todo.objects.filter(due_date__gte=datetime.now().date(), owner = request.user.id).exclude(id__in = urgent_todo_ids).exclude(is_completed = True).order_by('-due_date'))

        urgent_todo_count = len(urgent_todo)

        if urgent_todo_count < 10:
            final_result = urgent_todo + due_todo
            if len(final_result) > 10:
                final_result = final_result[:10]
        else:
            final_result = urgent_todo[:10]
        
        todo = ToDoGetSerializer(final_result, many=True, context=context).data        

        try:
            recent_obj = CompletionDetails.objects.filter(owner = request.user.id).order_by('-created_at')
            if len(recent_obj) > 5:
                recent_obj = recent_obj[:5]
            recent_activities = GetCompletionDetailsSerializer(recent_obj, many=True).data
        except:
            recent_activities = []
        # recent_activities = []

        response_data = {
            "self_challenge":self_challenge,
            "friend_challenge":friend_challenge,
            "todo":todo,
            "recent_activities":recent_activities
        }

        # for tes in response_data['self_challenge']['up_coming']:
        #     if tes['is_challenge_completed'] is True:
        #         print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #         print(tes.id)
        #         print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #     else:
        #         print('=====================================')

        return Response({"data":response_data, "message":"Search Data Fetched Successfully.", "status":200}, status=200)





class UpdateType(APIView):
    @swagger_auto_schema(
        operation_description="Type Update API",
        operation_summary="Type Update API",
        request_body=TypeSerializer,
    )
    def put(self, request, id=None, format=None):   
        print(request.data)
        response = Response()
        try:
            todo_to_update = Type.objects.get(id=id)
        except Type.DoesNotExist:
            return Response({"data":None, "message":"Type Does not Exist", "status":400}, status=400)
        serializer = TypeSerializer(instance=todo_to_update,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        

        response.data = {
            'message': 'Type Updated Successfully',
            'data': serializer.data
        }

        return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
class DeleteType(APIView):

    def delete(self, request, id, format=None):
        try:
            todo_to_delete =  Type.objects.get(id=id)
        except Type.DoesNotExist:
            return Response({"data":None, 'message': 'Type does not exist.', "status":400 }, status = 400)

        todo_to_delete.delete()
        return Response({"data":None, 'message': 'Type Deleted Successfully.', "status":200 }, status = 200)


class GetAllNumbersList(APIView):

    # queryset = Type.objects.all()
    # user = openapi.Parameter(
    #     "user",
    #     in_=openapi.IN_QUERY,
    #     description="user",
    #     type=openapi.TYPE_STRING,
    # )

    # """Decorator with parameter swagger auto schema"""

    # @swagger_auto_schema(manual_parameters=[ user])
    @csrf_exempt
    def get(self, request):
        data = request.GET
        user_id = request.user.id
        list_obj = {}
        earned_points = 0
        try:
            all_friend_challenge = GoalDetail.objects.filter(challenge__owner__id = user_id).exclude(challenge__challenger__id = user_id)
            for point in all_friend_challenge:
                if point.points is not None:
                    earned_points += int(point.points)
        except:
            pass
        list_obj['total_friend_challenge_points'] = earned_points
        if user_id:
            list_obj['total_todo'] = Todo.objects.filter(owner = user_id).count()
            list_obj['total_type'] = Type.objects.filter(user = user_id).count()
            list_obj['total_challenges_with_friends'] = FriendChallenge.objects.filter(~Q(owner=F('challenger')), owner = user_id).count()
            list_obj['total_pomodoro'] = Pomodoro.objects.filter(user = user_id).count()
            list_obj['total_challenge'] = FriendChallenge.objects.filter(owner = user_id, challenger = user_id).count()
        else:
            list_obj['total_todo'] = Todo.objects.filter(owner = None).count()
            list_obj['total_type'] = Type.objects.filter(user = None).count()
            list_obj['total_challenges_with_friends'] = FriendChallenge.objects.filter(owner = user_id, challenger = user_id).count()
            list_obj['total_pomodoro'] = Pomodoro.objects.filter(user = None).count()
            list_obj['total_challenge'] = FriendChallenge.objects.filter(owner = None).count()

        return Response({"data":list_obj, "message":"Type Fetched Successfully", "status":200}, status=200)

class GetProfile(APIView):
    # queryset = Type.objects.all()
    user = openapi.Parameter(
        "user",
        in_=openapi.IN_QUERY,
        description="user",
        type=openapi.TYPE_STRING,
    )

    """Decorator with parameter swagger auto schema"""

    @swagger_auto_schema(manual_parameters=[ user])
    @csrf_exempt
    def get(self, request):
        data = request.GET
        user_id = data.get('owner_id')
        list_obj = {}
        
        if user_id:
            list_obj['total_todo'] = ToDoGetSerializer(Todo.objects.filter(owner = user_id), many=True).data
            list_obj['total_type'] = GetTypeSerializer(Todo.objects.filter(user = user_id), many=True).data
            list_obj['total_pomodoro'] = PomodoroSerializer(Todo.objects.filter(user = user_id), many=True).data
            list_obj['total_challenge'] = FriendChallengeCreateSerializer(Todo.objects.filter(owner = user_id), many=True).data
        else:
            list_obj['total_todo'] = ToDoGetSerializer(Todo.objects.filter(owner = None), many=True).data
            list_obj['total_type'] = GetTypeSerializer(Type.objects.filter(user = user_id), many=True).data
            list_obj['total_pomodoro'] = PomodoroSerializer(Pomodoro.objects.filter(user = user_id), many=True).data
            list_obj['total_challenge'] = FriendChallengeCreateSerializer(FriendChallenge.objects.filter(owner = user_id), many=True).data

        return Response({"data":list_obj, "message":"Type Fetched Successfully", "status":200}, status=200)


class GetTagsByOwnersIDView(APIView):

    permission_classes = (AllowAny,)
    @csrf_exempt
    def get(self,request):
        tag_obj = Tags.objects.filter(Q(owner = request.user.id) | Q(owner__isnull = True))
        serializer = GetTagSerializer(tag_obj, many=True)
        return Response({"data":serializer.data, "message":"Get Fetched Successfully.", "status":200}, status=200)