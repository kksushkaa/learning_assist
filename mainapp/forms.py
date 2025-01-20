from typing import Any
from django.forms import ModelForm
from mainapp.models import Task, MyUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from mainapp.models import Status


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control ', 'placeholder':'Введите логин'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите пароль'}))
    class Meta:
        model = MyUser
        fields = ['username', 'password']


class UserRegForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control ', 'placeholder':'Введите логин'}))
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name','password1', 'password2']


class TaskAddForm(ModelForm):
    # настройка формы
    
    duration_good = forms.CharField(label='Продолжительность', widget = forms.TextInput(attrs={'class':'form-control '}))
    title = forms.CharField(label='Задача', widget = forms.TextInput(attrs={'class':'form-control '}))
    description = forms.CharField(label='Описание (необязательно)', widget = forms.Textarea(attrs={'class':'form-control '}))
    start_time = forms.CharField(label='Начало', widget = forms.DateTimeInput(attrs={'class':'form-control ', 'type':'datetime-local'}))
    class Meta:
        model = Task
        fields = ['title','description','start_time', 'duration_good']

    def clean_duration_good(self):
        time = self.cleaned_data['duration_good']
        spl_time = time.split(':')
        hours = int(spl_time[0])
        minutes = int(spl_time[1])
        return datetime.timedelta(hours=hours, minutes=minutes)
    
    def save(self, commit = True) -> Any:
        instance = super().save(commit = False)
        instance.duration = self.cleaned_data['duration_good']
        if commit:
            instance.save()
        return instance
    
class TaskEditForm(ModelForm):
    # настройка формы
    description = forms.CharField(widget=forms.Textarea(attrs={'id':'description_edit_field'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'title_edit_field'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), widget=forms.Select(attrs={'id':'status_edit_field'}))
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'id':'start_time_edit_field'}))
    duration_good = forms.CharField(widget=forms.TextInput(attrs={'id':'duration_good_edit_field'}))

    class Meta:
        model = Task
        fields = ['title','description','status','start_time', 'duration_good']

    def clean_duration_good(self):
        time = self.cleaned_data['duration_good']
        spl_time = time.split(':')
        hours = int(spl_time[0])
        minutes = int(spl_time[1])
        return datetime.timedelta(hours=hours, minutes=minutes)
    
    def save(self, commit = True) -> Any:
        instance = super().save(commit = False)
        instance.duration = self.cleaned_data['duration_good']
        if commit:
            instance.save()
        return instance
    