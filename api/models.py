from django.db import models

# Create your models here.
from datetime import date



class Notification(models.Model):
    """
    Модель рассылки
    """
    start_time = models.DateTimeField(auto_created=True, verbose_name='Дата старта')
    body = models.TextField(verbose_name='Текст сообщения')
    properties = models.JSONField(verbose_name='Фильтр свойств')
    end_time = models.DateTimeField(verbose_name='Дата окончания')


    def __str__(self):
        return str(self.id)

class Users(models.Model):
    """
    Модель пользователя
    """
    phone = models.BigIntegerField(verbose_name='номер телефона клиента')
    code = models.IntegerField(verbose_name='код мобильного оператора')
    tag = models.CharField(max_length=50, verbose_name='тег (произвольная метка)')
    timezone = models.IntegerField(verbose_name='часовой пояс')

    def __str__(self):
        return str(self.id)


class Msg(models.Model):
    """
    Модель сообщения
    """
    send_time = models.DateTimeField(auto_created=True, verbose_name='дата и время создания')
    state = models.CharField(max_length=50, verbose_name='статус отправки') # fail, pending, success
    user = models.ForeignKey(Users, verbose_name=("id клиента"), on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, verbose_name=("id рассылки"), on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
