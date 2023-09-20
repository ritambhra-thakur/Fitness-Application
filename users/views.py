from django.shortcuts import render 
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta, date
from django.template.loader import render_to_string
import random
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from users.models import Music, User, UserRevenueCatMapper, UserSubscriptionDetails
from users.serializers import GetMusicSerializer, GetUserDetailSerializer, CreateUserRevenueCatMapperSerializer, SaveUserSubscriptionDetailSerializer
from rest_framework.permissions import AllowAny
from todo.models import Todo
from challenge.models import FriendChallenge, GoalDetail
from utils.fetchSerializerErrors import fetch_serializer_error
from rest_framework.permissions import AllowAny, IsAuthenticated
from stretch.settings import DEFAULT_FROM_EMAIL

class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Forgot Password API",
        operation_summary="Forgot Password API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request, format=None):
        try:
            tz = pytz.timezone ('Asia/Kolkata')
            current_time = datetime.now (tz)
            user = User.objects.get(email=request.data["email"])
            otp = random.randint (1000, 9999)
            from_email=DEFAULT_FROM_EMAIL
            user.otp = otp
            user.otp_verification = False
            user.otp_send_time = current_time
            user.save()
            context = {"otp":otp}
            body_msg = render_to_string ('account/forgot-password-email.html', context)
            # body_msg=str(otp)
            msg = EmailMultiAlternatives ("Email Verification<Don't Reply>", body_msg, from_email, [user.email])
            msg.content_subtype = "html"  
            msg.send()
            return Response({"data":None, "code":200, "message": "OTP Sent Successfully."})
        except User.DoesNotExist:
            return Response({"data":None, "code":400, "message": "User Not Registered."})

#ForgetVerifyOTP
class ForgotVerifyOtpView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Verify OTP API",
        operation_summary="Verify OTP API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "otp": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request, format=None):
        tz = pytz.timezone ('Asia/Kolkata')
        current_time = datetime.now (tz)
        now_date = current_time.strftime ('%m/%d/%y')
        now_time = current_time.strftime ('%H:%M')

        otp = request.data['otp']
        user = None
        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            user = None
        if user:
            if user.otp_verification is True:
                return Response({"data": None, "code": 400, "message": "OTP Already Verified!"})
            if int(user.otp) == int(otp):
                otp_send_time = user.otp_send_time
                otp_send_time = otp_send_time.astimezone (tz) + timedelta (minutes=10)

                otp_date = datetime.strftime (otp_send_time, '%m/%d/%y')
                otp_time = datetime.strftime (otp_send_time, '%H:%M')

                if now_date == otp_date and now_time <= otp_time:
                    user.otp_verification = True
                    user.save()
                    return Response({"data": None, "code": 200, "message": "OTP Verified Successfully"})
                else:
                    return Response({"data": None, "code": 400, "message": "OTP Expired"})
            else:
                return Response({"data":None, "code":400, "message":"Wrong OTP"})
        else:
            return Response({"data": None, "code": 400, "message": "User Not Found!"})

#ChangePassword
class ChangePasswordView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Change Password API",
        operation_summary="Change Password API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    
    )

    def post(self, request, format=None):
        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            user = None
            return Response({"data":None, "code":400, "message":"User not Found!"})
        # if user.check_password(request.data["password"]):
        #     return Response({"data":None, "code":400, "message":""CANT_SET_SAME_PASSWORD""})
        if user.otp_verification is True:
            user.set_password(request.data["password"])
            user.save()
            #Adding email-notification for Customer user
            # body="Hi, you successfully changed your password."
            # title="Password Reset Successful."
            # if user.email_notification == True:
            #     TriggerEmailNotification(user.email, body, title)

            return Response({"data":None, "code":200, "message":"Password Changed Successfully"})
        else:
            return Response({"data": None, "code": 400, "message": "OTP Verified."})

class GetMusicListView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        music_obj = Music.objects.filter(is_active = True).order_by('sequence_id')
        serializer = GetMusicSerializer(music_obj, many=True)
        return Response({"data":serializer.data, "code":200, "message":"Music Fetched Successfully."})

    


class CreateMusicListView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Music Create API",
        operation_summary="Music Create API",
        request_body=GetMusicSerializer
    )
    
    def post(self, request, format=None):
        # music_obj = Music.objects.all()
        serializer = GetMusicSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "code":200, "message":"Music Created Successfully."})
        else:
            return Response({"data":serializer.errors, "code":200, "message":"Some Error Occured."})

class UpdateDefaultSound(APIView):

    def put(self, request, pk, format=None):
        try:
            request.user.default_sound = Music.objects.get(id = pk)
            request.user.save()
            return Response({"data":None, "code":200, "message":"Default Music Set Successfully."})
        except Music.DoesNotExist:
            return Response({"data":None, "code":200, "message":"Music Does Not Exist."})

class GetProfileByTokenView(APIView):

    def put(self, request, format=None):
        serializer = GetUserDetailSerializer(request.user)
        return Response({"data":serializer.data, "code":200, "message":"Default Music Set Successfully."})


class GetProfileDetailView(APIView):

    def get(self, request, format=None):
        user_id = request.user.id 

        username = request.user.full_name

        total_completed_todo = Todo.objects.filter(owner = user_id, is_completed = True).count()
        total_self_challenge = FriendChallenge.objects.filter(owner = user_id, challenger=user_id)
        total_completed_self_challenges = 0
        for self_challenge in total_self_challenge:
            completed_goals = GoalDetail.objects.filter(challenge = self_challenge.id, is_completed = True).count()
            if int(completed_goals) == int(self_challenge.timeline.number_of_days):
                total_completed_self_challenges+=1

        total_friend_challenge = FriendChallenge.objects.filter(owner = user_id).exclude(challenger=user_id)
        total_completed_friend_challenges = 0
        for friend_challenge in total_friend_challenge:
            completed_goals = GoalDetail.objects.filter(challenge = friend_challenge.id, is_completed = True).count()
            if int(completed_goals) == int(friend_challenge.timeline.number_of_days):
                total_completed_friend_challenges+=1

        #points calculation
        earned_points = 0
        all_friend_challenge = GoalDetail.objects.filter(challenge__owner__id = user_id).exclude(challenge__challenger__id = user_id)
        
        for point in all_friend_challenge:
            if point.points is not None:
                earned_points += int(point.points)
        
        resp = {
            "username" : username,
            "total_completed_todo": total_completed_todo,
            "total_completed_self_challenges": total_completed_self_challenges,
            "total_completed_friend_challenges": total_completed_friend_challenges,
            "earned_points":earned_points,
            "total_points":25,

        }

        return Response({"data":resp, "message":"Goal Details Saved Successfully.", "status":200}, status=200)


class UpdateUsernameView(APIView):

    def put(self, request, format=None):
        if 'username' in request.data:
            request.user.full_name = request.data['username']
            request.user.save()
            return Response({"data":None, "message":"Username Updated Successfully.", "status":200}, status=200)
        else:
            return Response({"data":None, "message":"Please send all the mandatory fields!", "status":400}, status=400)

class DeleteUserView(APIView):

    def delete(self, request, format=None):
        try:
            user_obj = User.objects.get(id = request.user.id)
        except User.DoesNotExist:
            return Response({"data":None, "message":"User Not Found!", "status":400}, status=400)
        user_obj.delete()
        return Response({"data":None, "message":"User Deleted Successfully.", "status":200}, status=200)

def fetch_privacy_policies(request):
    return render(request, 'account/privacy_policy.html')

class SaveRevenueCatIDView(APIView):

    def post(self, request, format=None):
        serializer = CreateUserRevenueCatMapperSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data, "message":"Revenue Cat ID saved Successfully!", "status":200}, status=200)
        else:
            return Response({"data":None, "message":fetch_serializer_error(serializer.errors), "status":400}, status=400)


class RevenueCatWebhookView(APIView):

    def post(self, request, format=None):
        final_data = {}
        try:
            user_id = request.data['event']['app_user_id']
            user_obj = User.objects.get(id = user_id)
            final_data['user'] = request.data['event']['app_user_id']
        except User.DoesNotExist:
            return Response({"data":None, "message":"User Not Found!", "status":400}, status=400)
        except:
            return Response({"data":None, "message":"Some Error Occured", "status":400}, status=400)
        if request.data['event']['type'] == 'CANCELLATION' or request.data['event']['type'] == 'EXPIRATION':
            # sub_obj = UserSubscriptionDetails.objects.filter(user = user_obj.id)
            # for sub in sub_obj:
            #     if sub.webhook_response['event']['original_transaction_id'] == request.data['event']['original_transaction_id']:
            #         sub.is_active = False
            #         sub.save()
            final_data['starts_on'] = None
            final_data['ends_on'] = None
            final_data['webhook_response'] = request.data
            final_data['is_active'] = False
            final_data['event_type'] = request.data['event']['type']
            
            serializer = SaveUserSubscriptionDetailSerializer(data = final_data)
            if serializer.is_valid():
                serializer.save()
                # old_sub_obj = UserSubscriptionDetails.objects.filter(user = user_obj.id).update(is_active = False)
                return Response({"data":None, "message":"Subscription Cancelled Successfully!", "status":200}, status=200)
            else:
                return Response({"data":None, "message":"Something went Wrong!!", "status":400}, status=400)    
            

        else:
            
            try:
                final_data['starts_on'] = request.data['event']['purchased_at_ms']
                final_data['ends_on'] = request.data['event']['expiration_at_ms']
                final_data['webhook_response'] = request.data
                final_data['event_type'] = request.data['event']['type']
            except:
                return Response({"data":None, "message":"Some Error Occured in processing response from Revenue Cat!", "status":400}, status=400)
            
            # req_data = json.dumps(str(request.data))
            # print(request.data)
            serializer = SaveUserSubscriptionDetailSerializer(data = final_data)
            if serializer.is_valid():
                serializer.save()
                old_sub_obj = UserSubscriptionDetails.objects.filter(user = user_obj.id).exclude(id = serializer.data['id']).update(is_active = False)
                # old_sub_obj.save()

                return Response({"data":serializer.data, "message":"Subscription Details Saved Successfully!", "status":200}, status=200)
            else:
                print('------------------------ in else')
                return Response({"data":None, "message":serializer.errors, "status":400}, status=400)



class TestRevenueCatWebhookView(APIView):


    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        data = request.data
        return Response({"data":None, "message":"Subscription Details Saved Successfully!", "status":200}, status=200)