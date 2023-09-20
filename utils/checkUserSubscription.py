from users.models import User, UserSubscriptionDetails
from todo.models import Todo
from pomodoro.models import Pomodoro
from challenge.models import FriendChallenge, FriendInvitationChallange
import time

def check_user_subscription(request, check_type):
    sub_obj = UserSubscriptionDetails.objects.filter(user = request.user.id, is_active = True).exclude(event_type = 'CANCELLATION').exclude(event_type = 'EXPIRATION').order_by('-created_at')
    active_sub = False
    if sub_obj.count() == 0:
        active_sub = False
    else:
        sub_end_timestamp = sub_obj[0].ends_on
        current_timestamp = time.time()
        if current_timestamp > sub_end_timestamp:
            return {"result":False, "detail":"Your Premium Subscription has expired, Please buy a Premium Plan to continue your Subscription!"}
        else:
            active_sub = True
    
    if active_sub is True:
        return {"result":True, "detail":"Active Subscription Found Successfully!"}
    else:
        if check_type == 1:
            check_count = Todo.objects.filter(owner = request.user.id).count()
            print(check_count)
            if check_count >= 3:
                return {"result":False, "detail":"Todo Limit Exceeded, Please buy a Premium Plan!"}
            else:
                return_message = "{} Todo left in Free Trial".format(str(3-check_count))
                return {"result":True, "detail":return_message}
        elif check_type == 2:
            check_count = Pomodoro.objects.filter(user = request.user.id).count()
            if check_count >= 3:
                return {"result":False, "detail":"Pomodoro Limit Exceeded, Please buy a Premium Plan!"} 
            else:
                return_message = "{} Pomodoro left in Free Trial".format(str(3-check_count))
                return {"result":True, "detail":return_message}
        elif check_type == 3:
            check_count = FriendChallenge.objects.filter(owner = request.user.id, challenger = request.user.id).count() #Self Challenge
            if check_count >= 3:
                return {"result":False, "detail":"Self Challenges Limit Exceeded, Please buy a Premium Plan!"}
            else:
                return_message = "{} Self Challenges left in Free Trial".format(str(3-check_count))
                return {"result":True, "detail":return_message}
        elif check_type == 4:
            check_count = FriendChallenge.objects.filter(owner = request.user.id).exclude(challenger = request.user.id).count() #Friend Challenge
            if check_count >= 2:
                return {"result":False, "detail":"Friend Challenges Limit Exceeded, Please buy a Premium Plan!"}
            else:
                return_message = "{} Friend Challenges left in Free Trial".format(str(2-check_count))
                return {"result":True, "detail":return_message}
        else:
            return {"result":False, "detail":"Incorrect Check Type"}

def check_invitation_count(friend_challenge_owner_id):
    sub_obj = UserSubscriptionDetails.objects.filter(user = friend_challenge_owner_id, is_active = True).exclude(event_type = 'CANCELLATION').exclude(event_type = 'EXPIRATION').order_by('-created_at')
    active_sub = False
    if sub_obj.count() == 0:
        active_sub = False
    else:
        sub_end_timestamp = sub_obj[0].ends_on
        current_timestamp = time.time()
        if current_timestamp > sub_end_timestamp:
            return {"result":False, "detail":"Your Premium Subscription has expired, Please buy a Premium Plan to continue your Subscription!"}
        else:
            active_sub = True
    
    if active_sub is True:
        return {"result":True, "detail":"Active Subscription Found Successfully!"}
    else:
        invitation_count = FriendInvitationChallange.objects.filter(owner = friend_challenge_owner_id, is_accepted = True).count()
        if invitation_count >= 2:
            return {"result":False, "detail":"Your Friend's limit for Inviting people to Friend Challenge has exceeded, Please suggest him to buy a Premium Plan."}
        else:
            return {"result":True, "detail":"{} Invites Left in Free Trial"} 