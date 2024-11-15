from django.db import models
from django.contrib.auth.models import User

'''
Написать список всех таблиц и полей БД
'''
class Status(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return f'{self.id}. {self.name}'


class Task(models.Model):
    '''
    пользователь
    время начала
    время конца
    статус
    '''
    title = models.CharField(max_length=256)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.id}. {self.title}'

