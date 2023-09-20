from challenge.models import CompletionDetails
from common.serializers import CreateCompletionDetailsSerializer

def save_completion_details(task_type, task_id, user_id):
    data = {"task_type":task_type,"owner":user_id}
    if int(task_type) == 1:
        try:
            comp_obj = CompletionDetails.objects.get(todo = task_id)
            return False
        except:
            data['todo'] = task_id
    elif int(task_type) == 2:
        try:
            comp_obj = CompletionDetails.objects.get(pomodoro = task_id)
            return False
        except:
            data['pomodoro'] = task_id
    elif int(task_type) == 3:
        try:
            comp_obj = CompletionDetails.objects.get(self_challenge = task_id)
            return False
        except:
            data['self_challenge'] = task_id
    elif int(task_type) == 4:
        try:
            comp_obj = CompletionDetails.objects.get(friend_challenge = task_id)
            return False
        except:
            data['friend_challenge'] = task_id
    else:
        return "Incorrect Task Type"


    serializer = CreateCompletionDetailsSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return True
    else:
        return str(serializer.errors)

    

