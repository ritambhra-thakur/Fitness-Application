from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from drf_yasg import openapi

from rest_framework.permissions import AllowAny, IsAuthenticated
import django_filters
from django_filters import rest_framework as filters

# import facebook
from pyfacebook import GraphAPI
from datetime import date
from utils.pointsCalculator import calc_points


from challenge.models import ChallengeUser, FriendChallenge, FriendInvitationChallange, GoalDetail, ChallengeCompletionMessage, ChallengeMessages
from challenge.serializers import AcceptInvitationChallangeSerializer, FriendChallengeCreateSerializer, FriendInvitationChallangeSerializer, GetFriendChallengeSerializer, CreateupdateGoalsDetailsSerializer, GetInvitationResponseSerializer, SaveInvitationResponseSerializer, CreateChallengeMessageSerializer, GetChallengeMessageSerializer
from todo.models import Todo
from users.permission import IsOwnerOrReadOnly
from django.db.models import Q, F

from users.models import SocialProfile, User
from utils.fetchSerializerErrors import fetch_serializer_error
from utils.checkUserSubscription import check_user_subscription, check_invitation_count

# Infff
import imp
import math
# from app.response import ResponseBadRequest, ResponseNotFound, ResponseOk
from django.conf import settings
from django.db.models import F, Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from django.http.response import Http404
# from app.response import ResponseBadRequest, ResponseNotFound, ResponseOk
# from app.util import custom_get_object, custom_get_pagination
# from user.models import Media, Profile, Token, User

# from .models import EmailTemplate
# from .serializers import EmailTemplatesSerializer

class FriendChallengeViewSets(viewsets.ModelViewSet):
    serializer_class = FriendChallengeCreateSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = FriendChallenge.objects.filter(owner=self.request.user)
        return queryset

class FriendInvitationChallangeAPIView(generics.ListCreateAPIView):
    serializer_class = FriendInvitationChallangeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    
    def get_queryset(self):
        queryset = FriendInvitationChallange.objects.filter(owner=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'status': True}, status=status.HTTP_201_CREATED)

class AcceptInvitationChallangeAPIView(generics.RetrieveAPIView):
    serializer_class = AcceptInvitationChallangeSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = FriendInvitationChallange.objects.all()
    lookup_field = 'pk'
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field


        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        if self.request.user.is_authenticated:
            if obj.email == self.request.request.user.email:
                ChallengeUser.objects.create(
                    challenge = FriendChallenge.objects.get(id=obj.challenge.id),
                    user=self.request.user,
                )
            else:
                raise APIException('YOU Either not authenticated or the invitation email is wrong !')

        return obj

class GetMyFacebookFriendList(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # more details can be here: https://facebook-sdk.readthedocs.io/en/latest/api.html
        social_profile = SocialProfile.objects.get(owner=self.request.user)
        # graph = facebook.GraphAPI(
        #     access_token=social_profile.facebook_access_token,
        #     version="2.12",
        #     # app_secret=getattr(settings, "FACEBOOK_INTEGRATION_SECRET_KEY")
        # )
        graph = GraphAPI(
            access_token=social_profile.facebook_access_token,
            app_id=getattr(settings, "FACEBOOK_INTEGRATION_CLIENT_ID"),
            app_secret=getattr(settings, "FACEBOOK_INTEGRATION_SECRET_KEY"),
            oauth_flow=True
        )
        friends = graph.get_connection(object_id='me', connection='friends')

        return Response(friends)

# class GetFriendChallenge(APIView):

#     def get(self, request, id, format=None):
#         if id:
#             item = FriendChallenge.objects.get(id=id)
#             print(item)
#             serializer = FriendChallengeCreateSerializer(item)
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

#         items = FriendChallenge.objects.all()
#         serializer = FriendChallengeCreateSerializer(items, many=True)
#         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


# class GetAllFriendChallenge(APIView):

#     queryset = FriendChallenge.objects.all()
#     owner = openapi.Parameter(
#         "owner",
#         in_=openapi.IN_QUERY,
#         description="owner",
#         type=openapi.TYPE_STRING,
#     )

#     """Decorator with parameter swagger auto schema"""

#     @swagger_auto_schema(manual_parameters=[ owner])
#     @csrf_exempt
#     def post(self, request):
#         data = request.GET
#         if 'owner' not in data:
#             return Response({"data":None, "message":"Please specify Owner ID", "status":400}, status=400)
#         friends_challenge_obj = FriendChallenge.objects.filter(owner = data['owner'])
#         serializer = FriendChallengeCreateSerializer(friends_challenge_obj, many=True)
#         return Response({"data":serializer.data, "message":"Friend Challenges Fetched Successfully", "status":200}, status=200)
    


# class CreateFriendChallenge(APIView):

#     @swagger_auto_schema(
#         operation_description="Friend challenge Create API",
#         operation_summary="Friend challenge Create API",
#         request_body=FriendChallengeCreateSerializer,
#     )
#     def post(self, request, format=None):
#         data = request.data
#         serializer = FriendChallengeCreateSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
#         else:
#             return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)


# class UpdateFriendChallenge(APIView):
#     @swagger_auto_schema(
#         operation_description="Friend  Challenge Update API",
#         operation_summary="Friend  Challenge Update API",
#         request_body=FriendChallengeCreateSerializer,
#     )
#     def put(self, request, pk=None, format=None):   
#         print(request.data)
#         response = Response()
#         try:
#             todo_to_update = FriendChallenge.objects.get(pk=pk)
#         except FriendChallenge.DoesNotExist:
#             response.data = {
#             'message': 'Challenge Does not Exist',
#             'data': None
#         }
#             return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)
#         serializer = FriendChallengeCreateSerializer(instance=todo_to_update,data=request.data, partial=True)

#         serializer.is_valid(raise_exception=True)

#         serializer.save()

        

#         response.data = {
#             'message': 'Challenge Updated Successfully',
#             'data': serializer.data
#         }

#         return Response({"data":serializer.data, "message":"OK", "status":200}, status=200)
# class DeleteFriendChallenge(APIView):

#     def delete(self, request, pk, format=None):
#         todo_to_delete =  FriendChallenge.objects.get(pk=pk)

#         todo_to_delete.delete()

#         return Response({
#             'message': 'Challenge Deleted Successfully'
#         })


class GetSelfChallenge(APIView):

    def get(self, request, id=None):
        if 'date' in request.GET:
            context = {'date':request.GET['date']}
        else:
            context = {'date': date.today()}
        context['request'] = request
        if id:
            item = FriendChallenge.objects.filter(id=id)
            serializer = GetFriendChallengeSerializer(item, many=True, context = context)
            return Response({"data":serializer.data, "message":"Self Challenge Fetched Successfully", "status":200}, status=200)

        items = FriendChallenge.objects.all().order_by('-id')
        serializer = GetFriendChallengeSerializer(items, many=True, context=context)
        return Response({"data":serializer.data, "message":"Self Challenge Fetched Successfully", "status":200}, status=200)



class GetFriendChallenge(APIView):

    def get(self, request, id=None):

        if 'date' in request.GET:
            context = {'date':request.GET['date']}
        else:
            context = {'date': date.today()}
        context['request'] = request
        
        if id:
            item = FriendChallenge.objects.filter(id=id)
            serializer = GetFriendChallengeSerializer(item, many=True, context = context)
            return Response({"data":serializer.data, "message":"Self Challenge Fetched Successfully", "status":200}, status=200)

        if 'owner' not in request.GET:
            return Response({"data":None, "message":"Please specify Owner ID", "status":400}, status=400)

        items = FriendChallenge.objects.filter(~Q(owner=F('challenger')), owner = request.GET['owner']).order_by('-id')
        serializer = GetFriendChallengeSerializer(items, many=True, context=context)
        return Response({"data":serializer.data, "message":"Self Challenge Fetched Successfully", "status":200}, status=200)



class GetAllSelfChallenge(APIView):

    queryset = FriendChallenge.objects.all()
    owner = openapi.Parameter(
        "owner",
        in_=openapi.IN_QUERY,
        description="owner",
        type=openapi.TYPE_STRING,
    )

    """Decorator with parameter swagger auto schema"""

    @swagger_auto_schema(manual_parameters=[ owner])
    @csrf_exempt
    def post(self, request):
        data = request.GET
        if 'date' in request.data:
            context = {"date":request.data['date']}
        else:
            context = {"date":  date.today()}
        p_date = request.data.get('date')
        if 'owner' not in data:
            return Response({"data":None, "message":"Please specify Owner ID", "status":400}, status=400)

        if p_date:
            friends_challenge_obj = FriendChallenge.objects.filter(start_date = p_date, owner = data['owner'], challenger = data['owner']).order_by('-id')
        else:
            friends_challenge_obj = FriendChallenge.objects.filter(owner = data['owner'], challenger = data['owner']).order_by('-id')
        count = FriendChallenge.objects.filter(owner = data['owner']).count()
        
        friends_challenge_obj = friends_challenge_obj.order_by('-created_at')
        serializer = GetFriendChallengeSerializer(friends_challenge_obj, many=True, context = context)
        return Response({"data":serializer.data, "count":count, "message":"Self Challenge Fetched Successfully", "status":200}, status=200)

class GetAllFriendChallenge(APIView):

    queryset = FriendChallenge.objects.all()
    owner = openapi.Parameter(
        "owner",
        in_=openapi.IN_QUERY,
        description="owner",
        type=openapi.TYPE_STRING,
    )

    """Decorator with parameter swagger auto schema"""

    @swagger_auto_schema(manual_parameters=[ owner])
    @csrf_exempt
    def post(self, request):
        data = request.data
        if 'date' in request.data:
            context = {"date":request.data['date'], "request":request}
        else:
            context = {"date":  date.today(), "request":request}
        p_date = request.data.get('date')
        if 'owner' not in data:
            return Response({"data":None, "message":"Please specify Owner ID", "status":400}, status=400)

        if p_date:
            friends_challenge_obj = FriendChallenge.objects.filter(~Q(owner=F('challenger')), start_date = p_date, owner = data['owner']).order_by('-id')
        else:
            friends_challenge_obj = FriendChallenge.objects.filter(~Q(owner=F('challenger')), owner = data['owner']).order_by('-id')
        

        friends_challenge_obj = friends_challenge_obj.order_by('-created_at')
        serializer = GetFriendChallengeSerializer(friends_challenge_obj, many=True, context = context)
        return Response({"data":serializer.data, "message":"Self Challenge Fetched Successfully", "status":200}, status=200)

class CreateSelfChallenge(APIView):

    @swagger_auto_schema(
        operation_description="Self Challenge Create API",
        operation_summary="Self Challenge Create API",
        request_body=FriendChallengeCreateSerializer,
    )
    def post(self, request, format=None):
        data = request.data
        serializer = FriendChallengeCreateSerializer(data=data)

        if serializer.is_valid():
            if 'challenger' not in data: #Friend Challenge
                check_resp = check_user_subscription(request, 4)
            elif data['owner'] == data['challenger']: #Self Challenge
                check_resp = check_user_subscription(request, 3)
            else: #Friend Challenge
                check_resp = check_user_subscription(request, 4)
            if check_resp['result'] is True:
                serializer.save()
                resp_data = GetFriendChallengeSerializer(FriendChallenge.objects.get(id = serializer.data['id'])).data
                return Response({"data":resp_data, "message":"Self Challenge Created Successfully.", "status":200}, status=200)
            else:
                return Response({"data":None, "message":check_resp['detail'] , "status":400}, status=400)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)

class UpdateSelfChallenge(APIView):
    @swagger_auto_schema(
        operation_description="Self Challenge Update API",
        operation_summary="Self Challenge Update API",
        request_body=FriendChallengeCreateSerializer,
    )
    def put(self, request, pk=None, format=None):   
        print(request.data)
        response = Response()
        try:
            todo_to_update = FriendChallenge.objects.get(pk=pk)
        except FriendChallenge.DoesNotExist:
            return Response({"data":None, "message":"Self Challenge Does not Exist", "status":400}, status=400)
        serializer = FriendChallengeCreateSerializer(instance=todo_to_update,data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        resp_data = GetFriendChallengeSerializer(FriendChallenge.objects.get(id = serializer.data['id'])).data

        

        response.data = {
            'message': 'Self Challenge Updated Successfully',
            'data': resp_data
        }

        return Response({"data":serializer.data, "message":"Self Challenge Updated Successfully.", "status":200}, status=200)
class DeleteSelfChallenge(APIView):

    def delete(self, request, pk, format=None):
        todo_to_delete =  FriendChallenge.objects.get(pk=pk)

        todo_to_delete.delete()

        return Response({"data":None, "message":"Self Challenge Deleted Successfully", "status":200}, status=200)

class DeleteSelfChallengeByOnwer(APIView):
    def delete(self, request, format=None):
        data = request.GET
        if 'owner' not in data:
            return Response({"data":None, "message":"Please specify Owner ID", "status":400}, status=400)

        friends_challenge_obj = FriendChallenge.objects.filter(owner = data['owner'])
        friends_challenge_obj.delete()
        return Response({"data":None, "message":"All Self Challenge Deleted Successfully", "status":200}, status=200)

class AcceptChallengeInviteView(APIView):

    def post(self, request, format=None):

        data = request.data
        invitation_id = data['invitation_id']
        try:
            invitation_obj = FriendInvitationChallange.objects.get(id = invitation_id)
        except FriendInvitationChallange.DoesNotExist:
            return Response({"data":None, "message":"Invitation Does Not Exist!", "status":400}, status=400)
        
        if invitation_obj.is_accepted is True:
            return Response({"data":None, "message":"Invitation Already Accepted!", "status":400}, status=400)
        elif invitation_obj.is_accepted is False:
            return Response({"data":None, "message":"Invitation Already Declined!", "status":400}, status=400)
        
        exisiting_check = FriendChallenge.objects.filter(owner = invitation_obj.invitee.id, challenger = invitation_obj.owner.id, parent_challenge = invitation_obj.challenge.id)
        if exisiting_check.count() > 0:
            return Response({"data":None, "message":"Already accepted this challenge!", "status":400}, status=400)



        # challenge_obj = FriendChallenge.objects.get(id = data['challenge'])
        # if challenge_obj.owner is not None and challenge_obj.challenger is not None:
        #     return Response({"data":None, "message":"Only supports Friend Challenges!", "status":400}, status=400)
        
        if data['is_accepted'] is True:
            sub_check = check_invitation_count(invitation_obj.owner.id)
            if sub_check['result'] is False:
                return Response({"data":None, "message":sub_check['detail'], "status":400}, status=400)
            invitation_obj.is_accepted = True
            invitation_obj.save()
            

            friend_challenge_request = {
                "name": invitation_obj.challenge.name,
                "owner" : invitation_obj.invitee.id,
                "challenger": invitation_obj.owner.id,
                "start_date": invitation_obj.challenge.start_date,
                "category": invitation_obj.challenge.category.id,
                "type": invitation_obj.challenge.type.id,
                "time": invitation_obj.challenge.time,
                "timeline": invitation_obj.challenge.timeline.id,
                "goal_value": invitation_obj.challenge.goal_value,
                "goal_unit": invitation_obj.challenge.goal_unit.id,
                "is_active": invitation_obj.challenge.is_active,
                "parent_challenge":invitation_obj.challenge.id
            }
            serializer = FriendChallengeCreateSerializer(data = friend_challenge_request)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "message":"Invitation Accepted Successfully.", "status":200}, status=200)
            else:
                return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)
        else:
            invitation_obj.is_accepted = False
            invitation_obj.save()
            return Response({"data":None, "message":"Invitation Declined Successfully.", "status":200}, status=200)

class CreateInvitaitonView(APIView):
    def post(self, request, format=None):
        request.data['invitee'] = request.user.id
        try:
            existing_invitation = FriendInvitationChallange.objects.get(owner = request.data['owner'], invitee = request.data['invitee'], challenge = request.data['challenge'])
            return Response({"data":None, "message":"Invitation Already Exists", "status":400}, status=400)
        except:
            pass
        serializer = SaveInvitationResponseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"Invitation Registered Successfully.", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)


class GetInvitaitonsView(APIView):

    def post(self, request, format=None):
        # if 'is_accepted' in request.data:
        #     is_accepted = request.data['is_accepted']
        #     invitation_obj = FriendInvitationChallange.objects.filter(invitee = request.user.id, is_accepted = is_accepted)
        # else:

        pending_invitation_obj = FriendInvitationChallange.objects.filter(invitee = request.user.id, is_accepted = None)
        accepted_invitation_obj = FriendInvitationChallange.objects.filter(invitee = request.user.id, is_accepted = True)

        pending_serializer = GetInvitationResponseSerializer(pending_invitation_obj, many=True).data
        accepted_serializer = GetInvitationResponseSerializer(accepted_invitation_obj, many=True).data
        data = {
            "pending_invitaitons":pending_serializer,
            "accepted_invitaitons":accepted_serializer
        }

        return Response({"data":data, "message":"Invitation Fetched Successfully.", "status":200}, status=200)
        

        
        

class CreateUpdateGoalDetails(APIView):

    def post(self, request, format=None):
        task_completed = float(request.data['goal_value'])
        try:
            existing_details = GoalDetail.objects.get(challenge = request.data['challenge'], date = request.data['date'])
            unit_obj = existing_details.challenge.goal_unit
        except GoalDetail.DoesNotExist:
            existing_details = None
            try:
                unit_obj = FriendChallenge.objects.get(id = request.data['challenge']).goal_unit
            except:
                return Response({"data":None, "message":"Challenge Does not Exist!", "status":400}, status=400)
        
        request.data['points'] = calc_points(unit_obj, task_completed)

        if existing_details is None:
            serializer = CreateupdateGoalsDetailsSerializer(data = request.data)
        else:
            serializer = CreateupdateGoalsDetailsSerializer(existing_details, data = request.data)

        if serializer.is_valid():
            serializer.save()
            
            completed_count = GoalDetail.objects.filter(is_completed=True, challenge = request.data['challenge']).count()
            try:
                challenge_obj = FriendChallenge.objects.get(id = request.data['challenge'])
                target_count = challenge_obj.timeline.number_of_days
                if int(target_count) == int(completed_count):
                    try:
                        if challenge_obj.owner.id == challenge_obj.challenger.id:
                            pop_up_obj = ChallengeCompletionMessage.objects.get(message_type = 1)
                        else:
                            pop_up_obj = ChallengeCompletionMessage.objects.get(message_type = 2)
                    except:
                        pop_up_obj = ChallengeCompletionMessage.objects.get(message_type = 2)
                    
                    message_obj = {"title":pop_up_obj.title, "body":pop_up_obj.body}
                    final_res = {"is_completed":True, "pop_up_details":message_obj}
                else:
                    message_obj = {"title":"", "body":""}
                    final_res = {"is_completed":False, "pop_up_details":message_obj}
            except:
                message_obj = {"title":"", "body":""}
                final_res = {"is_completed":False, "pop_up_details":message_obj}

            return Response({"data":serializer.data, "pop_up":final_res, "message":"Goal Details Saved Successfully.", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)




class DeleteAllSelfChallenges(APIView):

    def delete(self, request, format=None):
        user_id = request.user.id
        delete_obj = FriendChallenge.objects.filter(owner = user_id, challenger = user_id).delete()
        return Response({"data":None, "message":"All Self Challenge Deleted Successfully.", "status":200}, status=200)


class SendChallengeCompletionMessageView(APIView):

    def post(self, request, format=None):
        try:
            challenge_obj = FriendChallenge.objects.get(id = request.data['friend_challenge'])
            request.data['receiver'] = challenge_obj.challenger.id
        except Exception as e:
            print('---------------------------------')
            print(str(e))
            return Response({"data":None, "message":"Challenge Does Not Exist!", "status":400}, status=400)
        request.data['sender'] = request.user.id

        serializer = CreateChallengeMessageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"Message Sent Successfully.", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)


class GetChallengeCompletionMessageView(APIView):
    
    def get(self, request, format=None):
        message_obj = ChallengeMessages.objects.filter(Q(sender = request.user.id) | Q(receiver = request.user.id)).order_by('-id')
        context = {"request":request}
        serializer = GetChallengeMessageSerializer(message_obj, many=True, context = context)

        # setting recieved messages as read
        try:
            received_message_obj = ChallengeMessages.objects.filter(receiver = request.user.id, is_read = False).update(is_read = True)
            received_message_obj.save()
        except:
            pass
        return Response({"data":serializer.data, "message":"Messages Fetched Successfully.", "status":200}, status=200)

class GetUnReadMessageCount(APIView):

    def get(self, request, format=None):
        message_count = ChallengeMessages.objects.filter(receiver = request.user.id, is_read = False).count()
        return Response({"data":message_count, "message":"Un-Read Messages Count Fetched Successfully.", "status":200}, status=200)