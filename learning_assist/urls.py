"""
URL configuration for learning_assist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from mainapp.views import (
    index,
    schedule_view,
    todolist,
    assist,
    quiz,
    quiz_query_view,
    gpt_query_view,
    add_task_view,
    edit_task_view,
    get_task_info,
    logout_view,
    reg_view, 
    get_all_users_tasks,
    check_answers,
    delete_task
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("schedule", schedule_view),
    path("todolist", todolist),
    path("assist/gpt_query/", gpt_query_view),
    path("assist", assist),
    path("quiz", quiz),
    path("logout", logout_view),
    path("register", reg_view),
    path("quiz/quiz_query/", quiz_query_view),
    path("todolist/add_task_view", add_task_view),
    path("todolist/edit_task_view", edit_task_view),
    path("get_task_info/<int:task_id>", get_task_info), 
    path("delete_task/<int:task_id>", delete_task), 
    path("get_all_users_tasks", get_all_users_tasks),
    path("quiz/check_answers", check_answers)
]
