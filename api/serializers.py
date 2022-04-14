from rest_framework import serializers

from api.models import Msg, Notification, Users


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
        
class MsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Msg
        fields = '__all__'
        

