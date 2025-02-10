import datetime
from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from mainapp.models import MyUser, Status, Task


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control ", "placeholder": "Введите логин"}
        )
    )
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        )
    )

    class Meta:
        model = MyUser
        fields = ["username", "password"]


class UserRegForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control ", "placeholder": "Введите логин"}
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control ", "placeholder": "Введите почту "}
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control ", "placeholder": "Введите ваше имя "}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control ", "placeholder": "Введите пароль "}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control ", "placeholder": "Введите пароль ещё раз "}
        )
    )

    class Meta:
        model = MyUser
        fields = ["username", "email", "first_name", "password1", "password2"]


class TaskAddForm(ModelForm):
    # настройка формы

    duration_good = forms.CharField(
        label="Продолжительность",
        widget=forms.TextInput(attrs={"class": "form-control "}),
    )
    title = forms.CharField(
        label="Задача", widget=forms.TextInput(attrs={"class": "form-control "})
    )
    description = forms.CharField(
        label="Описание (необязательно)",
        widget=forms.Textarea(attrs={"class": "form-control "}),
        required=False
    )
    start_time = forms.CharField(
        label="Начало",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control ", "type": "datetime-local"}
        ),
    )

    class Meta:
        model = Task
        fields = ["title", "description", "start_time", "duration_good"]

    def clean_duration_good(self):
        time = self.cleaned_data["duration_good"]
        spl_time = time.split(":")
        hours = int(spl_time[0])
        minutes = int(spl_time[1])
        return datetime.timedelta(hours=hours, minutes=minutes)

    def save(self, commit=True) -> Any:
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data["duration_good"]
        if commit:
            instance.save()
        return instance


class TaskEditForm(ModelForm):
    # настройка формы
    description = forms.CharField(
        label="Описание (необязательно)",
        widget=forms.Textarea(attrs={"class": "form-control","id": "description_edit_field"}),
        required=False
    )
    title = forms.CharField(
        label="Задача", widget=forms.TextInput(attrs={"class": "form-control ", "id": "title_edit_field"})
    )

    status = forms.ModelChoiceField(
        label="Cтатус",
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={"class": "form-control ", "id": "status_edit_field"})
    )
    start_time = forms.CharField(
        label="Начало",
        widget=forms.DateTimeInput(
            attrs={"class": "form-control ", "type": "datetime-local", "id": "start_time_edit_field"}
        ),
    )
    duration_good = forms.CharField(
        label="Продолжительность",
        widget=forms.TextInput(attrs={"class": "form-control ", "id": "duration_good_edit_field"})
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "start_time", "duration_good"]

    def clean_duration_good(self):
        time = self.cleaned_data["duration_good"]
        spl_time = time.split(":")
        hours = int(spl_time[0])
        minutes = int(spl_time[1])
        return datetime.timedelta(hours=hours, minutes=minutes)

    def save(self, commit=True) -> Any:
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data["duration_good"]
        if commit:
            instance.save()
        return instance
