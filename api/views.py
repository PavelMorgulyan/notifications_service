from django.shortcuts import render
from api import serializers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.db.models import Q, Count
from django.utils import timezone
from api.utils import post_to_server


from api.models import Notification, Users, Msg
from api.serializers import NotificationSerializer, UserSerializer, Msg

class UserListView(APIView):
    """
    Endpoint создания пользователя.
    Принимает на вход параметр:
    :param
        user_id: id пользователя
    :return
        JSON вида {'id': user_id}
        Если пользователь уже существует, возвращает ID этого пользователя
        Если передаётся пустое поле создаёт нового пользователя
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
            users = Users.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)


class UserDetailsView(APIView):
    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404
    
    """
        Put: Обновление информации о пользователе
    """
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """
        delete: Удаление информации о пользователе
    """    
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationView(APIView):
    """
        Post: Создание 1 рассылки по id=pk
        
        Get: Просмотр всех рассылок
    """
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            if data['start_time'] < timezone.now() and timezone.now() < data['end_time']:
                serializer.save()
                post_to_server(data['id'], data['body'],  data['properties']) # !!! response (post) to io server https://probe.fbrq.cloud/v1 with jwt
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request):
        notification = Notification.objects.all()
        serializer = NotificationSerializer(notification, many=True)
        return Response(serializer.data)
    
    
class NotificationDetailView(APIView):
    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        notification = self.get_object(pk)
        serializer = NotificationSerializer(notification)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk, format=None):
        notification = self.get_object(pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    def put(self, request, pk, format=None):
        notification = self.get_object(pk)
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(APIView):
    '''
        Получение общей статистики по созданным рассылкам и количеству 
        отправленных сообщений по ним с группировкой по статусам
    '''
    def get(self, request):
        notification = Msg.objects\
            .values('notification', 'state')\
            .annotate(total_msg=Count('notification'))
        
        return Response(notification)


