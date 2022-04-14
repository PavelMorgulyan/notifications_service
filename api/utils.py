
import re
from api.models import Notification, Users, Msg
from api.serializers import NotificationSerializer, UserSerializer, MsgSerializer
import requests 
from django.utils import timezone
from rest_framework.response import Response
from django.http import Http404


def post_to_server(notification_id, body, properties):
    users = Users.objects.filter(tag=properties).all()
    for user in users:
        endpoint = 'https://probe.fbrq.cloud/v1/send/1'
        send_time = timezone.now()
        dataload = {"id": user['id'], "phone": user['phone'], "text": body}
        
        msg = create_msg(send_time, "pending", user['id'], notification_id)
        
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODA2MTYwNjksImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IlBhdmVsTWFyZ3VseWFuIn0.BjFhgS7gh97O-_TbKLRPsn1MULtKTT1S6ISK6BQnoHU"}
        
        # 1 - тестовый запрос post, юзер теперь подписан
        
        request = requests.post(endpoint, data=dataload, headers=headers) 
        if request.status_code == 200:
            update_state_message(msg)

def create_msg(send_time, state, user, notification):
    data = {'send_time': send_time, 'state': state, 'user':user, 'notification': notification}
    serializer = MsgSerializer(data=data)
    
    if serializer.is_valid():
        msg = serializer.save()
        print("Message was created")
        print(msg)
        return msg # Response(data, status=status.HTTP_201_CREATED)
    return "Message creation failed" # Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_object(self, pk):
    try:
        return Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        raise Http404

def update_state_message(msg):
    msg = Msg.objects.get_object(msg.id)
    serializer = MsgSerializer(data=msg)
    if serializer.is_valid():
        serializer.save()
        return "Message successfully updated" 
    